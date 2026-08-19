/-
  SpecSemantics.lean — machine-checked core of the order theory behind Spack's
  `Spec.satisfies` / `Spec.constrain`.

  Self-contained Lean 4 (no Mathlib).  The development mirrors the LaTeX note
  `spec-semantics.tex`:

  1. `Pre`         — preorders (satisfies is reflexive and transitive, nothing more).
  2. `Pre.equiv`   — mutual satisfaction `a ~ b`, proved an equivalence; the
                     antisymmetrization quotient `Pre.Q` is a partial order.
  3. `Meet`        — a partial binary meet (constrain): sound (lower bound),
                     greatest (GLB when defined), and total on compatible pairs
                     (defined whenever a common lower bound exists).  Idempotence,
                     commutativity, associativity hold up to `~`, and descend to
                     genuine equalities on the quotient.
  4. `Pre.ann`     — annotations invisible to the order (propagation policies
                     `%` vs `%%`): the quotient of the annotated preorder is
                     order-isomorphic to the quotient of the base preorder.
  5. `Pre.prod`    — binary products: nodes are finite products of dimensions.
  6. `flat`, `multi` — two dimension instances: flat domains with an
                     "unconstrained" top (names, os, platform, pinned values),
                     and multi-valued constraint sets as lists ordered by
                     reverse membership, whose quotient identifies reordered
                     and duplicated value lists.
  7. `Tree`, `TLe` — rooted edge-labelled trees with the simulation order used
                     by `satisfies` on the dependency DAG; reflexivity and
                     transitivity are proved, and edge annotations collapse.
-/

set_option autoImplicit false

namespace SpecSemantics

universe u v

/-! ### 1. Preorders -/

/-- A preorder: `satisfies` is reflexive and transitive.  Antisymmetry is *not*
    assumed; distinct spec representations may satisfy each other. -/
structure Pre (α : Type u) : Type u where
  le : α → α → Prop
  refl : ∀ a, le a a
  trans : ∀ {a b c}, le a b → le b c → le a c

variable {α : Type u} {β : Type v}

/-! ### 2. Mutual satisfaction and the antisymmetrization quotient -/

/-- `a ~ b` iff `a` satisfies `b` and `b` satisfies `a`. -/
def Pre.equiv (P : Pre α) (a b : α) : Prop := P.le a b ∧ P.le b a

theorem Pre.equiv_refl (P : Pre α) (a : α) : P.equiv a a := ⟨P.refl a, P.refl a⟩

theorem Pre.equiv_symm (P : Pre α) {a b : α} (h : P.equiv a b) : P.equiv b a :=
  ⟨h.2, h.1⟩

theorem Pre.equiv_trans (P : Pre α) {a b c : α} (h₁ : P.equiv a b) (h₂ : P.equiv b c) :
    P.equiv a c :=
  ⟨P.trans h₁.1 h₂.1, P.trans h₂.2 h₁.2⟩

/-- `~` as a `Setoid`, so we can form the quotient. -/
def Pre.setoid (P : Pre α) : Setoid α :=
  ⟨P.equiv, ⟨P.equiv_refl, P.equiv_symm, P.equiv_trans⟩⟩

/-- The set of specs modulo mutual satisfaction, `S/~`. -/
def Pre.Q (P : Pre α) : Type u := Quotient P.setoid

/-- The class of `a` in `S/~`. -/
def Pre.cls (P : Pre α) (a : α) : P.Q := Quotient.mk P.setoid a

/-- Equivalent specs are one point of `S/~`. -/
theorem Pre.sound (P : Pre α) {a b : α} (h : P.equiv a b) : P.cls a = P.cls b :=
  Quot.sound h

/-- `le` is `~`-invariant, hence descends to the quotient. -/
theorem Pre.le_congr (P : Pre α) {a a' b b' : α}
    (ha : P.equiv a a') (hb : P.equiv b b') : P.le a b ↔ P.le a' b' :=
  ⟨fun h => P.trans ha.2 (P.trans h hb.1),
   fun h => P.trans ha.1 (P.trans h hb.2)⟩

/-- The induced order on `S/~`. -/
def Pre.qle (P : Pre α) : P.Q → P.Q → Prop :=
  Quotient.lift₂ P.le (fun _ _ _ _ ha hb => propext (P.le_congr ha hb))

theorem Pre.qle_mk (P : Pre α) (a b : α) : P.qle (P.cls a) (P.cls b) ↔ P.le a b :=
  Iff.rfl

theorem Pre.qle_refl (P : Pre α) (x : P.Q) : P.qle x x :=
  Quotient.inductionOn x (fun a => P.refl a)

theorem Pre.qle_trans (P : Pre α) {x y z : P.Q}
    (h₁ : P.qle x y) (h₂ : P.qle y z) : P.qle x z :=
  Quotient.inductionOn₃ x y z (fun _ _ _ h₁ h₂ => P.trans h₁ h₂) h₁ h₂

/-- The point of the quotient: on `S/~` the order is antisymmetric, so `S/~`
    is a partial order. -/
theorem Pre.qle_antisymm (P : Pre α) {x y : P.Q}
    (h₁ : P.qle x y) (h₂ : P.qle y x) : x = y :=
  Quotient.inductionOn₂ x y (fun _ _ h₁ h₂ => Quot.sound ⟨h₁, h₂⟩) h₁ h₂

/-! ### 3. Partial meets: `constrain` -/

/-- A partial binary meet.  `meet a b = none` models `constrain` raising on an
    unsatisfiable pair.  The three laws:

    * `sound`    — a defined meet is a common lower bound (the result satisfies
                   both operands);
    * `greatest` — a defined meet is above every common lower bound;
    * `total`    — the meet is defined whenever *some* common lower bound
                   exists (constrain only raises on genuinely disjoint specs). -/
structure Meet {α : Type u} (P : Pre α) : Type u where
  meet : α → α → Option α
  sound : ∀ {a b m}, meet a b = some m → P.le m a ∧ P.le m b
  greatest : ∀ {a b m c}, meet a b = some m → P.le c a → P.le c b → P.le c m
  total : ∀ {a b c}, P.le c a → P.le c b → ∃ m, meet a b = some m

namespace Meet

variable {P : Pre α} (M : Meet P)

/-- Idempotence up to `~`: `a ∧ a` is defined and equivalent to `a`. -/
theorem idem (a : α) : ∃ m, M.meet a a = some m ∧ P.equiv m a := by
  obtain ⟨m, hm⟩ := M.total (P.refl a) (P.refl a)
  exact ⟨m, hm, (M.sound hm).1, M.greatest hm (P.refl a) (P.refl a)⟩

/-- Commutativity of definedness. -/
theorem comm_def {a b : α} : (∃ m, M.meet a b = some m) ↔ (∃ m, M.meet b a = some m) := by
  constructor <;> intro h <;> obtain ⟨m, hm⟩ := h
  · exact M.total (M.sound hm).2 (M.sound hm).1
  · exact M.total (M.sound hm).2 (M.sound hm).1

/-- Commutativity up to `~` on the defined domain. -/
theorem comm {a b m n : α} (h₁ : M.meet a b = some m) (h₂ : M.meet b a = some n) :
    P.equiv m n :=
  ⟨M.greatest h₂ (M.sound h₁).2 (M.sound h₁).1,
   M.greatest h₁ (M.sound h₂).2 (M.sound h₂).1⟩

/-- Associativity up to `~`, including definedness: if `(a ∧ b) ∧ c` is
    defined then so is `a ∧ (b ∧ c)`, with equivalent results. -/
theorem assoc {a b c ab abc : α}
    (h₁ : M.meet a b = some ab) (h₂ : M.meet ab c = some abc) :
    ∃ bc abc', M.meet b c = some bc ∧ M.meet a bc = some abc' ∧ P.equiv abc abc' := by
  have habc_ab : P.le abc ab := (M.sound h₂).1
  have habc_a : P.le abc a := P.trans habc_ab (M.sound h₁).1
  have habc_b : P.le abc b := P.trans habc_ab (M.sound h₁).2
  have habc_c : P.le abc c := (M.sound h₂).2
  obtain ⟨bc, hbc⟩ := M.total habc_b habc_c
  have habc_bc : P.le abc bc := M.greatest hbc habc_b habc_c
  obtain ⟨abc', habc'⟩ := M.total habc_a habc_bc
  refine ⟨bc, abc', hbc, habc', M.greatest habc' habc_a habc_bc, ?_⟩
  -- abc' is a common lower bound of a, b, c, hence ≤ ab, hence ≤ abc.
  have h₁' : P.le abc' a := (M.sound habc').1
  have hbc' : P.le abc' bc := (M.sound habc').2
  have h₂' : P.le abc' b := P.trans hbc' (M.sound hbc).1
  have h₃' : P.le abc' c := P.trans hbc' (M.sound hbc).2
  exact M.greatest h₂ (M.greatest h₁ h₁' h₂') h₃'

/-- The meet is a `~`-congruence in definedness. -/
theorem congr_def {a a' b b' : α} (ha : P.equiv a a') (hb : P.equiv b b') :
    (∃ m, M.meet a b = some m) ↔ (∃ m, M.meet a' b' = some m) := by
  constructor <;> intro h <;> obtain ⟨m, hm⟩ := h
  · exact M.total (P.trans (M.sound hm).1 ha.1) (P.trans (M.sound hm).2 hb.1)
  · exact M.total (P.trans (M.sound hm).1 ha.2) (P.trans (M.sound hm).2 hb.2)

/-- The meet is a `~`-congruence in the result. -/
theorem congr {a a' b b' m m' : α} (ha : P.equiv a a') (hb : P.equiv b b')
    (h : M.meet a b = some m) (h' : M.meet a' b' = some m') : P.equiv m m' := by
  constructor
  · exact M.greatest h' (P.trans (M.sound h).1 ha.1) (P.trans (M.sound h).2 hb.1)
  · exact M.greatest h (P.trans (M.sound h').1 ha.2) (P.trans (M.sound h').2 hb.2)

/-! On the quotient `S/~` the partial meet becomes a partial operation with
    *equational* laws. -/

private theorem qmeet_respects {a a' b b' : α}
    (ha : P.setoid.r a a') (hb : P.setoid.r b b') :
    (M.meet a b).map P.cls = (M.meet a' b').map P.cls := by
  cases h : M.meet a b with
  | none =>
    cases h' : M.meet a' b' with
    | none => rfl
    | some m' =>
      obtain ⟨m, hm⟩ := (M.congr_def ha hb).mpr ⟨m', h'⟩
      rw [h] at hm
      cases hm
  | some m =>
    obtain ⟨m', h'⟩ := (M.congr_def ha hb).mp ⟨m, h⟩
    rw [h']
    simp only [Option.map]
    exact congrArg some (P.sound (M.congr ha hb h h'))

/-- The induced meet on `S/~`. -/
def qmeet : P.Q → P.Q → Option P.Q :=
  Quotient.lift₂ (fun a b => (M.meet a b).map P.cls)
    (fun _ _ _ _ ha hb => M.qmeet_respects ha hb)

theorem qmeet_mk (a b : α) : M.qmeet (P.cls a) (P.cls b) = (M.meet a b).map P.cls :=
  rfl

/-- On the quotient, idempotence is an equality. -/
theorem qmeet_idem (x : P.Q) : M.qmeet x x = some x := by
  refine Quotient.inductionOn x (fun a => ?_)
  show (M.meet a a).map P.cls = some (P.cls a)
  obtain ⟨m, hm, hme⟩ := M.idem a
  rw [hm]
  simp only [Option.map]
  exact congrArg some (P.sound hme)

/-- On the quotient, commutativity is an equality. -/
theorem qmeet_comm (x y : P.Q) : M.qmeet x y = M.qmeet y x := by
  refine Quotient.inductionOn₂ x y (fun a b => ?_)
  show (M.meet a b).map P.cls = (M.meet b a).map P.cls
  cases h : M.meet a b with
  | none =>
    cases h' : M.meet b a with
    | none => rfl
    | some n =>
      obtain ⟨m, hm⟩ := M.comm_def.mpr ⟨n, h'⟩
      rw [h] at hm
      cases hm
  | some m =>
    obtain ⟨n, hn⟩ := M.comm_def.mp ⟨m, h⟩
    rw [hn]
    simp only [Option.map]
    exact congrArg some (P.sound (M.comm h hn))

/-- On the quotient, associativity is an equality of partial results
    (`Option.bind` chains the two applications). -/
theorem qmeet_assoc (x y z : P.Q) :
    (M.qmeet x y).bind (fun xy => M.qmeet xy z)
      = (M.qmeet y z).bind (fun yz => M.qmeet x yz) := by
  refine Quotient.inductionOn₃ x y z (fun a b c => ?_)
  show ((M.meet a b).map P.cls).bind (fun xy => M.qmeet xy (P.cls c))
      = ((M.meet b c).map P.cls).bind (fun yz => M.qmeet (P.cls a) yz)
  cases hab : M.meet a b with
  | none =>
    -- a ∧ b undefined: the left side is none; show the right side is too.
    simp only [Option.map, Option.bind]
    cases hbc : M.meet b c with
    | none => rfl
    | some bc =>
      show (none : Option P.Q) = (M.meet a bc).map P.cls
      cases habc : M.meet a bc with
      | none => rfl
      | some m =>
        -- m ≤ a and m ≤ bc ≤ b, so a ∧ b would be defined: contradiction.
        obtain ⟨k, hk⟩ :=
          M.total (M.sound habc).1 (P.trans (M.sound habc).2 (M.sound hbc).1)
        rw [hab] at hk
        cases hk
  | some ab =>
    simp only [Option.map, Option.bind]
    show (M.meet ab c).map P.cls
        = ((M.meet b c).map P.cls).bind (fun yz => M.qmeet (P.cls a) yz)
    cases habc : M.meet ab c with
    | none =>
      -- (a ∧ b) ∧ c undefined: no common lower bound of ab and c,
      -- hence the right-hand chain is undefined too.
      simp only [Option.map]
      cases hbc : M.meet b c with
      | none => rfl
      | some bc =>
        simp only [Option.bind]
        show (none : Option P.Q) = (M.meet a bc).map P.cls
        cases habc' : M.meet a bc with
        | none => rfl
        | some m =>
          have hm_ab : P.le m ab :=
            M.greatest hab (M.sound habc').1 (P.trans (M.sound habc').2 (M.sound hbc).1)
          obtain ⟨k, hk⟩ := M.total hm_ab (P.trans (M.sound habc').2 (M.sound hbc).2)
          rw [habc] at hk
          cases hk
    | some abc =>
      obtain ⟨bc, abc', hbc, habc', he⟩ := M.assoc hab habc
      rw [hbc]
      simp only [Option.map, Option.bind]
      show some (P.cls abc) = (M.meet a bc).map P.cls
      rw [habc']
      simp only [Option.map]
      exact congrArg some (P.sound he)

end Meet

/-! ### 4. Annotations invisible to the order (`%` vs `%%`) -/

/-- Attach an annotation of type `π` that `le` ignores — e.g. the propagation
    policy on an edge, which constrains solver optimality, not the solution
    set. -/
def Pre.ann (P : Pre α) (π : Type v) : Pre (α × π) where
  le x y := P.le x.1 y.1
  refl x := P.refl x.1
  trans h₁ h₂ := P.trans h₁ h₂

/-- Two annotated values are `~`-equivalent iff their payloads are: the
    annotation is erased by mutual satisfaction.  In particular `%foo ~ %%foo`. -/
theorem Pre.ann_equiv (P : Pre α) {π : Type v} (a b : α) (p q : π) :
    (P.ann π).equiv (a, p) (b, q) ↔ P.equiv a b :=
  Iff.rfl

/-- An order isomorphism between two quotiented preorders. -/
structure OrderIso {α : Type u} {β : Type v} (P : Pre α) (Q : Pre β) : Type (max u v) where
  toFun : P.Q → Q.Q
  invFun : Q.Q → P.Q
  left_inv : ∀ x, invFun (toFun x) = x
  right_inv : ∀ y, toFun (invFun y) = y
  mono : ∀ {x y}, P.qle x y → Q.qle (toFun x) (toFun y)
  mono_inv : ∀ {x y}, Q.qle x y → P.qle (invFun x) (invFun y)

/-- Quotienting erases the annotation completely: `(S × Π)/~` is order-
    isomorphic to `S/~`.  The propagation-policy dimension is invisible in the
    partial order of specs. -/
def Pre.annIso (P : Pre α) (π : Type v) [Inhabited π] : OrderIso (P.ann π) P where
  toFun := Quotient.lift (fun x : α × π => P.cls x.1)
    (fun _ _ h => Quot.sound h)
  invFun := Quotient.lift (fun a => (P.ann π).cls (a, default))
    (fun _ _ h => Quot.sound h)
  left_inv x := Quotient.inductionOn x (fun a => Quot.sound ⟨P.refl a.1, P.refl a.1⟩)
  right_inv y := Quotient.inductionOn y (fun a => Quot.sound ⟨P.refl a, P.refl a⟩)
  mono {x y} h := Quotient.inductionOn₂ x y (fun _ _ h => h) h
  mono_inv {x y} h := Quotient.inductionOn₂ x y (fun _ _ h => h) h

/-! ### 5. Products: a node is a finite product of dimensions -/

/-- The product preorder: pointwise satisfaction — node-level `satisfies`
    requires every dimension to satisfy. -/
def Pre.prod (P : Pre α) (Q : Pre β) : Pre (α × β) where
  le x y := P.le x.1 y.1 ∧ Q.le x.2 y.2
  refl x := ⟨P.refl x.1, Q.refl x.2⟩
  trans h₁ h₂ := ⟨P.trans h₁.1 h₂.1, Q.trans h₁.2 h₂.2⟩

/-- Pointwise partial meets give a partial meet on the product: `constrain`
    merges dimension by dimension and fails if any dimension is disjoint. -/
def Meet.prod {P : Pre α} {Q : Pre β} (M : Meet P) (N : Meet Q) :
    Meet (P.prod Q) where
  meet x y :=
    match M.meet x.1 y.1, N.meet x.2 y.2 with
    | some m, some n => some (m, n)
    | _, _ => none
  sound {x y m} h := by
    cases h₁ : M.meet x.1 y.1 with
    | none => simp [h₁] at h
    | some a =>
      cases h₂ : N.meet x.2 y.2 with
      | none => simp [h₁, h₂] at h
      | some b =>
        simp only [h₁, h₂] at h
        cases h
        exact ⟨⟨(M.sound h₁).1, (N.sound h₂).1⟩, ⟨(M.sound h₁).2, (N.sound h₂).2⟩⟩
  greatest {x y m c} h hc₁ hc₂ := by
    cases h₁ : M.meet x.1 y.1 with
    | none => simp [h₁] at h
    | some a =>
      cases h₂ : N.meet x.2 y.2 with
      | none => simp [h₁, h₂] at h
      | some b =>
        simp only [h₁, h₂] at h
        cases h
        exact ⟨M.greatest h₁ hc₁.1 hc₂.1, N.greatest h₂ hc₁.2 hc₂.2⟩
  total {x y c} h₁ h₂ := by
    obtain ⟨m, hm⟩ := M.total h₁.1 h₂.1
    obtain ⟨n, hn⟩ := N.total h₁.2 h₂.2
    exact ⟨(m, n), by simp [hm, hn]⟩

/-! ### 6. Dimension instances -/

/-! #### Flat domains with an unconstrained top

`none` is the absent constraint (an unset name, os, or platform, an
undeclared single-valued variant); `some x` pins the value. -/

def flat (α : Type u) : Pre (Option α) where
  le x y := y = none ∨ x = y
  refl _ := Or.inr rfl
  trans {a b c} h₁ h₂ := by
    cases h₂ with
    | inl h => exact Or.inl h
    | inr h =>
      cases h₁ with
      | inl h' => exact Or.inl (h ▸ h')
      | inr h' => exact Or.inr (h'.trans h)

/-- In a flat domain, `constrain` keeps the more constrained side and fails on
    a pinned-value clash. -/
def flatMeet (α : Type u) [DecidableEq α] : Meet (flat α) where
  meet x y :=
    match x, y with
    | none, b => some b
    | some a, none => some (some a)
    | some a, some b => if a = b then some (some a) else none
  sound {x y m} h := by
    match x, y with
    | none, b =>
      cases h
      exact ⟨Or.inl rfl, Or.inr rfl⟩
    | some a, none =>
      cases h
      exact ⟨Or.inr rfl, Or.inl rfl⟩
    | some a, some b =>
      by_cases hab : a = b
      · simp only [hab] at h
        cases h
        exact ⟨Or.inr (by rw [hab]), Or.inr rfl⟩
      · simp [hab] at h
  greatest {x y m c} h h₁ h₂ := by
    match x, y with
    | none, b =>
      cases h
      exact h₂
    | some a, none =>
      cases h
      exact h₁
    | some a, some b =>
      by_cases hab : a = b
      · simp only [hab] at h
        cases h
        exact h₂
      · simp [hab] at h
  total {x y c} h₁ h₂ := by
    match x, y with
    | none, b => exact ⟨b, rfl⟩
    | some a, none => exact ⟨some a, rfl⟩
    | some a, some b =>
      -- c satisfies both pinned values, so they agree.
      cases h₁ with
      | inl h => cases h
      | inr h =>
        cases h₂ with
        | inl h' => cases h'
        | inr h' =>
          have hab : a = b := Option.some.inj (h.symm.trans h')
          exact ⟨some a, by simp [hab]⟩

/-! #### Multi-valued variant constraints

A constraint is the list of required values (`foo=a,b`).  `S ≤ T` iff `S`
requires every value `T` does.  The order ignores order and multiplicity, so
the quotient identifies e.g. `[1, 2]` and `[2, 1, 1]` — value lists denote
finite sets.  The meet is concatenation and never fails. -/

def multi (α : Type u) : Pre (List α) where
  le S T := ∀ x, x ∈ T → x ∈ S
  refl _ _ h := h
  trans h₁ h₂ _ hx := h₁ _ (h₂ _ hx)

def multiMeet (α : Type u) : Meet (multi α) where
  meet S T := some (S ++ T)
  sound {S T m} h := by
    cases h
    exact ⟨fun x hx => List.mem_append.mpr (Or.inl hx),
           fun x hx => List.mem_append.mpr (Or.inr hx)⟩
  greatest {S T m c} h h₁ h₂ := by
    cases h
    intro x hx
    cases List.mem_append.mp hx with
    | inl hS => exact h₁ x hS
    | inr hT => exact h₂ x hT
  total _ _ := ⟨_, rfl⟩

/-- Reordered, duplicated value lists are one point of `S/~`. -/
example : (multi Nat).equiv [1, 2] [2, 1, 1] := by
  constructor <;> intro x hx <;> simp at hx <;> rcases hx with h | h <;> simp [h]

/-! ### 7. The dependency DAG: simulation order on rooted labelled trees

`a.satisfies(b)` requires, for every dependency constraint (edge) of `b`, an
edge of `a` whose label satisfies it and whose child recursively satisfies the
constraint's child.  We model the unfolding of the DAG as a rooted tree with
node payloads in `ν` and edge labels in `ε` (children indexed by `Fin n`, with
labels and subtrees as two parallel functions to keep the type non-nested),
and state the simulation with an explicit witness map from the constraint's
edges to the candidate's. -/

inductive Tree (ν : Type u) (ε : Type v) : Type (max u v) where
  | node : ν → (n : Nat) → (Fin n → ε) → (Fin n → Tree ν ε) → Tree ν ε

namespace Tree

variable {ν : Type u} {ε : Type v}

/-- The simulation order.  `TLe P E s t`: the root of `s` satisfies the root of
    `t`, and a witness map sends every edge of `t` to an edge of `s` with a
    satisfying label and a recursively satisfying child. -/
inductive TLe (P : Pre ν) (E : Pre ε) : Tree ν ε → Tree ν ε → Prop where
  | node {a b : ν} {n m : Nat}
      {la : Fin n → ε} {ca : Fin n → Tree ν ε}
      {lb : Fin m → ε} {cb : Fin m → Tree ν ε}
      (f : Fin m → Fin n) :
      P.le a b →
      (∀ j, E.le (la (f j)) (lb j)) →
      (∀ j, TLe P E (ca (f j)) (cb j)) →
      TLe P E (.node a n la ca) (.node b m lb cb)

theorem TLe.refl (P : Pre ν) (E : Pre ε) : ∀ t : Tree ν ε, TLe P E t t := by
  intro t
  induction t with
  | node a n la ca ih =>
    exact TLe.node (fun j => j) (P.refl a) (fun j => E.refl _) (fun j => ih j)

theorem TLe.trans (P : Pre ν) (E : Pre ε) :
    ∀ {s t u : Tree ν ε}, TLe P E s t → TLe P E t u → TLe P E s u := by
  intro s t u h₁ h₂
  induction h₂ generalizing s with
  | @node b c m k lb cb lc cc g hbc hlab hsub ih =>
    cases h₁ with
    | node f hab hlab' hsub' =>
      exact TLe.node (fun j => f (g j)) (P.trans hab hbc)
        (fun j => E.trans (hlab' (g j)) (hlab j))
        (fun j => ih j (hsub' (g j)))

/-- The simulation order as a `Pre`: `satisfies` on dependency structures is a
    preorder. -/
def pre (P : Pre ν) (E : Pre ε) : Pre (Tree ν ε) where
  le := TLe P E
  refl := TLe.refl P E
  trans := TLe.trans P E

/-- Edge annotations invisible to the edge order are invisible to the tree
    order: two one-edge specs that differ only in the policy annotation on the
    edge (`%foo` vs `%%foo`) are mutually satisfying. -/
example {ν ε π : Type} (P : Pre ν) (E : Pre ε) (a b : ν) (e : ε) (p q : π)
    (hab : P.equiv a b) (t : Tree ν (ε × π)) :
    (Tree.pre P (E.ann π)).equiv
      (.node a 1 (fun _ => (e, p)) (fun _ => t))
      (.node b 1 (fun _ => (e, q)) (fun _ => t)) := by
  constructor
  · exact TLe.node (fun j => j) hab.1 (fun _ => E.refl e) (fun _ => TLe.refl _ _ t)
  · exact TLe.node (fun j => j) hab.2 (fun _ => E.refl e) (fun _ => TLe.refl _ _ t)

end Tree

end SpecSemantics
