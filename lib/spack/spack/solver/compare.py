#!/usr/bin/env spack-python

import spack.solver.asp as asp

import os
import argparse

# import clingo -- imported by driver?
import numpy
import spack.cmd
import spack.paths
import matplotlib.pyplot as plt


max_error_priority = 3

reweight_predicates = [
    "literal_not_solved",
    "build",
    "optimize_for_reuse",
    "requirement_weight",
    "build_priority",
    "version_weight",
    "variant_not_default",
    "provider_weight",
    "variant_default_not_used",
    "compiler_mismatch",
    "compiler_mismatch_required",
    "node_os_mismatch",
    "compiler_weight",
    "node_os_weight",
    "node_target_mismatch",
    "node_target_weight",
    # testing
    "depends_on",
    "version_declared",
    "internal_error",
]

debug_predicates = [
    "build_priority",
    "node_target_weight",
    "node_target_mismatch",
    "node_os_weight",
    "compiler_weight",
    "node_os_mismatch",
    "compiler_mismatch_required",
    "compiler_mismatch",
    "variant_default_not_used",
    "provider_weight",
    "variant_not_default",
    "version_weight",
    "attr",
    "requirement_weight",
    "requirement_has_weight",
    "opt_criterion",
    "literal_not_solved",
    "depth",
    "optimize_for_reuse",
    "depends_on",
    "version_declared",
    "package_target_weight",
    "version_default_value",
    "build",
    "error",
    "internal_error",
    "opt_criterion",  # necessarY?
]


class SpecNode(object):
    def __init__(self, name, parent=None):
        self.name = name
        self.children = []

        if parent == None:
            self.depth = 0
        else:
            self.depth = parent.depth + 1
            parent.add_child(self)

    def add_child(self, child):
        self.children.append(child)

    def print_tree(self, max_depth=10, level=0):
        print("\t" * level, self.name)
        for child in self.children:
            child.print_tree(max_depth, level + 1)


class TempResult(object):
    """Temporary result of a solve."""

    def __init__(self):
        self.weights = []
        self.depth = None
        self.symbols = None
        self.ranking = None

        self.attr_rules = []
        self.reweight_rules = []
        self.depth_rules = []
        self.depends_on = []

        self.specs = []  # list of root spec names as strings
        self.node_depths = {}  # dict of all nodes and static depths
        self.spec_trees = {}

    def truncate_weights(self):
        # get actual max depth
        max_depth = max(self.node_depths.values())
        print("truncating to actual max depth:", max_depth)

        costs = self.weights
        opt_criteria = asp.extract_functions(self.symbols, "opt_criterion")

        # borrowed from asp.build_criteria_names
        # ensure names of all criteria are unique
        names = {criterion.args[0] for criterion in opt_criteria}
        assert len(names) == len(opt_criteria), "names of optimization criteria must be unique"

        # split opt criteria into two lists
        fixed_criteria = [oc for oc in opt_criteria if oc.args[1] == "fixed"]
        leveled_criteria = [oc for oc in opt_criteria if oc.args[1] == "leveled"]

        # first non-error criterion
        solve_index = max_error_priority + 1

        # compute without needing max_depth from solve
        max_leveled_costs = (len(costs) - max_error_priority - 3) / 2
        assert max_leveled_costs * 2 == len(costs) - max_error_priority - 3
        assert max_leveled_costs % len(leveled_criteria) == 0
        max_leveled_costs = int(max_leveled_costs)

        n_leveled_costs = len(leveled_criteria) * (max_depth + 1)

        build_index = solve_index + 1 + max_leveled_costs
        fixed_costs = [costs[solve_index], costs[build_index]]

        build_costs = costs[solve_index + 1 : solve_index + 1 + n_leveled_costs]
        reuse_costs = costs[build_index + 1 : build_index + 1 + n_leveled_costs]
        assert len(build_costs) == len(reuse_costs) == n_leveled_costs

        return build_costs + reuse_costs

    def spectree(self, root):

        r = SpecNode(root)

        # breadth first traversal of depends_on tree
        parents = [r]
        self.node_depths[r.name] = r.depth
        while parents != []:
            p = parents[0]
            for afun in self.depends_on:
                # second condition removes duplicates and keeps copy at the highest level
                if afun.args[0] == p.name and afun.args[1] not in self.node_depths:
                    child = SpecNode(afun.args[1], p)
                    parents.append(child)
                    self.node_depths[child.name] = child.depth
            parents.remove(p)

        return r

    def new_depth_rules(self, newd):
        rules = []

        for node, depth in self.node_depths.items():
            if depth > newd:
                depth = newd
            rules.append('depth("' + node + '", ' + str(depth) + ").")

        return rules

    def setup(self, cost, symbols, depth, ranking):

        self.weights = cost
        self.depth = depth
        self.ranking = ranking
        self.symbols = symbols

        self.attr_rules = asp.extract_functions(symbols, "attr")

        # rules for reweighting are in global list but must also include attr
        self.reweight_rules = [str(e) + "." for e in self.attr_rules]
        for p in reweight_predicates:
            for e in asp.extract_functions(symbols, p):
                self.reweight_rules.append(str(e) + ".")

        # initial depth rules, used for debugging
        for d in ["depth"]:
            for e in asp.extract_functions(symbols, d):
                self.depth_rules.append(str(e) + ".")

        # used to regenerate depths statically
        self.depends_on = asp.extract_functions(symbols, "depends_on")

        # TODO: this list already exists somewhere
        for a in self.attr_rules:
            if a.args[0] == "root":
                self.specs.append(a.args[1])

        # generate spec tree for each spec (stored in dictionary by root)
        for spec in self.specs:
            self.spec_trees[spec] = self.spectree(spec)

    def add_to_control(self, control, new_depth):
        """Add all necessary reweighting rules to control object."""
        for p in self.reweight_rules:
            control.add("rule", [], p)

        for d in self.new_depth_rules(new_depth):
            control.add("depth", [], d)

    def print_depths(self):
        """Debugging tool to view initial depths."""
        for d in self.depth_rules:
            print(d)

    def print_program(self, filename):
        """Debugging tool to view all rooles used for reweighting"""
        f = open(filename, "w")

        for p in debug_predicates:
            for a in asp.extract_functions(self.symbols, p):
                f.write(str(a) + ".\n")

        f.close()


class DAGCompare(object):
    def __init__(self, specs):
        self.specs = spack.cmd.parse_specs(specs)
        self.parent_dir = os.path.join(spack.paths.module_path, "solver")
        self.min_depth = 1
        self.depths = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        # defined in setup_all
        self.initial_results = []  # list of the top TempResult objects at depth 1
        self.at_depth_results = (
            {}
        )  # dictionary of best TempResult for at every depth in self.depths
        self.reweights = {}  # dictionary of depth, list of weights for each initial result

    def initial_solve(self, depth, count):
        """Run solve setup for the given specs to check for errors. Then solve fully with modified display and max_depth to generate TempResult objects."""
        specs = self.specs

        # setup_only to check for errors
        solver = asp.Solver()
        solver.solve(specs, setup_only=True)

        # solve with specific max_depth and detailed display
        driver = solver.driver
        driver.control.load(os.path.join(self.parent_dir, "concretize.lp"))
        driver.control.load(os.path.join(self.parent_dir, "os_compatibility.lp"))
        driver.control.load(os.path.join(self.parent_dir, "display-recreate.lp"))

        driver.control.add("depth", [], "#const max_depth = " + str(depth) + ".")
        driver.control.ground([("base", [])])

        models = []
        cores = []

        def on_model(model):
            # shown variable determines if results from display.lp are included in the model representation
            models.append((model.cost, model.symbols(shown=True, terms=True)))

        solve_kwargs = {
            #            "assumptions": driver.assumptions,
            "on_model": on_model,
            "on_core": cores.append,
        }

        solve_res = driver.control.solve(**solve_kwargs)

        results = []

        if solve_res.satisfiable:

            for idx, (min_cost, curr_model) in enumerate(sorted(models)):
                # only retrieve up to count solutions
                if idx >= count:
                    break

                # create TempResult object
                res = TempResult()
                res.setup(min_cost, curr_model, depth, idx)

                results.append(res)

        assert len(results) > 0, "No solutions generated for initial solve."

        best_result = results[0]

        return results

    def reweight_solve(self, result, new_depth, filename=None):
        """Generate weights for the given result evaluated at the given depth."""
        assert result.depth <= new_depth, "Reweight failed - cannot reweight to smaller depth."

        solver = asp.Solver()
        driver = solver.driver

        driver.control = asp.default_clingo_control()

        driver.control.load(os.path.join(self.parent_dir, "minimize.lp"))
        # driver.control.load(os.path.join(self.parent_dir, "display-recreate.lp"))

        # add result predicates to control object
        result.add_to_control(driver.control, new_depth)

        driver.control.add("depth", [], "#const max_depth = " + str(new_depth) + ".")

        driver.control.ground([("base", []), ("depth", []), ("attr", []), ("rule", [])])

        models = []
        cores = []

        def on_model(model):
            # shown variable determines if results from display.lp are included in the model representation
            models.append((model.cost, model.symbols(shown=True, terms=True)))

        solve_kwargs = {
            #            "assumptions": driver.assumptions,
            "on_model": on_model,
            "on_core": cores.append,
        }

        solve_res = driver.control.solve(**solve_kwargs)

        assert solve_res.satisfiable, "Reweight failed - no solutions found."
        assert len(models) == 1, "Reweight failed - more than one solution found."

        model = min(sorted(models))

        (weights, symbols) = model

        result = TempResult()
        result.symbols = symbols
        # result.print_program("reweight_program.lp")

        criteria = asp.extract_functions(symbols, "opt_criterion")

        l1 = len(weights)
        l2 = len(self.at_depth_results[new_depth].weights)

        if l1 != l2:
            print("Reweight failed - wrong length weight vector.")

        return weights

    def setup_all(self):
        self.initial_results = self.initial_solve(1, 10)

        for d in self.depths:
            self.at_depth_results[d] = self.initial_solve(d, 1)[0]
            self.reweights[d] = [self.reweight_solve(r, d) for r in self.initial_results]

    # def plot_comparison(self, result, depth, depth_specific):
    #     """Plot line for best model at depth in comparison with line for each initial model reweighted"""
    #     new_weights = reweight_solve(result, depth)
    #     nweights = len(new_weights)

    #     x = numpy.arange(1, nweights + 1)
    #     comp_weights = depth_specific.weights

    #     plt.title("comparison at depth=" + str(depth))
    #     plt.plot(x,new_weights)
    #     plt.plot(x,comp_weights)

    #     plt.legend(["regenerated", "true depth"])
    #     plt.show()

    # def plot_norm(results, deep_results, depth):
    #     assert depth > 1, "cannot compare with depth less than 2."

    #     d = deep_results[depth-self.min_depth]

    #     deep_weights = d.weights
    #     x = numpy.arange(1, len(deep_weights) + 1)
    #     plt.title("comparison at depth=" + str(depth))

    #     dweights = numpy.array(deep_weights)

    #     for r in results:
    #         new_weights = numpy.array(reweight_solve(r, depth))
    #         comparison = new_weights - dweights
    #         plt.plot(x, comparison)

    #     plt.legend(["model"+str(i) for i in range(0, len(results))])
    #     plt.show()

    def rank_at_depth(self, depth):
        """Rank all initial results at the given depth according to lexicographical order."""
        assert depth in self.depths, "invalid depth request"
        weights = []

        for idx, r in enumerate(self.initial_results):
            new_weights = self.reweights[depth][1][idx]
            weights.append((idx, new_weights))

        sorted_weights = sorted(weights, key=lambda l: tuple(l[1]))

        ordering = [x[0] for x in sorted_weights]
        return ordering

    def rank(self):
        for d in self.depths:
            print((d, self.rank_at_depth(d)))

    def plot_compare_best(self, d):

        best_model_idx = self.rank_at_depth(d)[0]
        best_model_weights = self.reweights[d - self.min_depth][1][best_model_idx]

        x = numpy.arange(1, len(best_model_weights) + 1)

        plt.title("Best model comparison at depth " + str(d))
        plt.plot(x, best_model_weights)
        plt.plot(x, self.at_depth_results[d - self.min_depth].weights)
        plt.legend(["initial model #" + str(best_model_idx), "model at depth"])
        plt.show()

    def first_deviation(self, model, d):

        at_depth = self.at_depth_results[d - self.min_depth].weights

        diff = numpy.array(self.reweights[d - self.min_depth][1][model]) - numpy.array(at_depth)

        for index, ele in enumerate(diff):
            if ele != 0:
                return (index, ele)

        return None

    # def sorted_weights(self, init_res, depth):
    #     weights_at_depth = []
    #     for idx, r in enumeinit_res:
    #         w = reweights(depth)
    #         weights_at_depth.append((r.ranking, w))

    #     return sorted(weights_at_depth, key=lambda l : tuple(l[1]))

    # def sort_all(self,init_res):
    #     depths = self.depths
    #     all_orderings = []
    #     for depth in depths:
    #         ordering = []
    #         for x in sorted_weights(self.initial_results, depth):
    #             ordering.append(x[0])
    #             all_orderings.append((depth, ordering))

    #     return all_orderings


# depths = range(min_depth, 3)
# initial_results = (initial_solve(specs, 1, 10))
# depth_specific_results = [initial_solve(specs, d, 1)[0] for d in depths]

# ordering = sort_all(initial_results, depths)
# initial_results[0].print_program()


# for (depth, order) in ordering:
#     best_model_key = order[0]

#     if depth == 1:
#         assert best_model_key == 0

#     print("At depth:", depth, "model #", best_model_key, "performs best.")


#     #build rank order based on differences from depth specific solution
#     differences = []
#     best_weight = []
#     old_weights = depth_specific_results[depth-min_depth].weights

#     for idx, res in enumerate(initial_results):
#         new_weights = reweight_solve(res, depth)

#         if idx == best_model_key:
#             best_weight = (idx, new_weights)

#         difference = numpy.array(new_weights) - numpy.array(old_weights)
#         differences.append((idx, difference))


#     sorted_differences = sorted(differences, key=lambda l : tuple(l[1]))
#     ranked_differences = (depth, [x[0] for x in sorted_differences])

#     distance_norm = (depth, [numpy.linalg.norm(x[1]) for x in sorted_differences])
#     print("ranked differences: ", ranked_differences)
#     print("distance from dss:  ", distance_norm)

#     x = numpy.arange(1, len(best_weight[1]) + 1)
#     plt.plot(x, numpy.array(best_weight[1]))
#     plt.plot(x, numpy.array(old_weights))

#     plt.show()

#     #distances = [(i, distance(initial_results[i], depth_specific_results[depth-2], depth)) for i in range(0, len(initial_results))]
#     #print("distances from depth specific result:")
#     #print(distances)
#     #print(distance(initial_results[best_model_keyA], depth_specific_results[depth-2], depth))
#     #print(distance(initial_results[1], depth_specific_results[depth-2], depth))

#     #print("orig - at depth: ", numpy.array(reweight_solve(initial_results[best_model_key], depth)) -  numpy.array(depth_specific_results[depth-2].weights))
#     #print("mod0 - at depth: ", numpy.array(reweight_solve(initial_results[0], depth)) -  numpy.array(depth_specific_results[depth-2].weights))
#     #dresult = depth_specific_results[depth-2]
