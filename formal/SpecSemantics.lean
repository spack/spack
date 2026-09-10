/-
  SpecSemantics.lean — the machine-checked order theory behind Spack's
  `Spec.satisfies` / `Spec.constrain`, developed on Mathlib (toolchain and
  dependency pinned in `lakefile.toml`; `lake build` checks it).  The
  development mirrors the LaTeX note `spec-semantics.tex`:

  1–2. Preorders and quotient — `satisfies` as a `Preorder`; specs modulo
       mutual satisfaction via `Antisymmetrization`.
  3. Partial meet             — `PartialMeet` (M1–M3) models `constrain`;
       descended to the quotient and totalized with `⊥` (`WithBot`), it is
       a `SemilatticeInf` with the equational laws as consequences.
  4. Annotations              — dimensions the order ignores (`%` vs `%%`)
       collapse in the quotient.
  5. Products                 — a node is a finite product of dimensions.
  6. Dimensions               — flat domains with an unconstrained top;
       multi-valued constraints as the dual `Finset` lattice.
  7. Simulation trees         — the order `satisfies` uses on the
       dependency DAG.
  8. Partial kernel           — the repo projection π_R: greatest fixed
       point below, adjunction with the R-valid states, meet commutation
       derived from the axioms; totalized, a `ClosureOperator` on the dual
       order.
-/
import Mathlib.Order.Antisymmetrization
import Mathlib.Order.Closure
import Mathlib.Order.WithBot
import Mathlib.Order.Hom.Basic
import Mathlib.Data.Finset.Lattice.Basic
import Mathlib.Data.Finset.Dedup

set_option autoImplicit false

namespace SpecSemantics

universe u v

variable {α : Type u} {β : Type v}

/-! ### 1–2. Preorders and the antisymmetrization quotient —

`satisfies` is a `Preorder` (reflexive, transitive, deliberately not
antisymmetric).  Mutual satisfaction is `AntisymmRel (· ≤ ·)`; the set of
specs modulo mutual satisfaction is `Antisymmetrization α (· ≤ ·)`; that it
is a partial order is Mathlib's instance. -/

/-- Specs modulo mutual satisfaction, `S/~`. -/
abbrev Q (α : Type u) [Preorder α] : Type u := Antisymmetrization α (· ≤ ·)

section Quotient

variable [Preorder α]

/-- The class of a spec in `S/~`. -/
abbrev cls (a : α) : Q α := toAntisymmetrization (· ≤ ·) a

/-- `S/~` is a partial order: reflexivity, transitivity, antisymmetry all
    come from the instance. -/
example : PartialOrder (Q α) := inferInstance

/-- The induced order agrees with the underlying one. -/
theorem cls_le_cls {a b : α} : (cls a : Q α) ≤ cls b ↔ a ≤ b :=
  toAntisymmetrization_le_toAntisymmetrization_iff

/-- Equivalent specs are one point of `S/~`. -/
theorem cls_eq_cls {a b : α} (h : AntisymmRel (· ≤ ·) a b) : (cls a : Q α) = cls b :=
  Quotient.sound' h

/-- Induction on classes, for the descent proofs below. -/
theorem Q.inductionOn {p : Q α → Prop} (x : Q α) (mk : ∀ a, p (cls a)) : p x :=
  Quotient.inductionOn' x mk

end Quotient

/-! ### 3. Partial meets: `constrain`

Mathlib has no partial binary meet; (M1)–(M3) axiomatize `constrain`
directly. -/

/-- A partial binary meet.  `meet a b = none` models `constrain` raising on
    an unsatisfiable pair.  (M1) `sound`: a defined meet is a common lower
    bound.  (M2) `greatest`: it is above every common lower bound.  (M3)
    `total`: it is defined whenever some common lower bound exists. -/
structure PartialMeet (α : Type u) [Preorder α] : Type u where
  meet : α → α → Option α
  sound : ∀ {a b m}, meet a b = some m → m ≤ a ∧ m ≤ b
  greatest : ∀ {a b m c}, meet a b = some m → c ≤ a → c ≤ b → c ≤ m
  total : ∀ {a b c}, c ≤ a → c ≤ b → ∃ m, meet a b = some m

namespace PartialMeet

variable [Preorder α] (M : PartialMeet α)

/-- Definedness is a `~`-congruence. -/
theorem congr_def {a a' b b' : α}
    (ha : AntisymmRel (· ≤ ·) a a') (hb : AntisymmRel (· ≤ ·) b b') :
    (∃ m, M.meet a b = some m) ↔ (∃ m, M.meet a' b' = some m) := by
  constructor <;> intro h <;> obtain ⟨m, hm⟩ := h
  · exact M.total (le_trans (M.sound hm).1 ha.1) (le_trans (M.sound hm).2 hb.1)
  · exact M.total (le_trans (M.sound hm).1 ha.2) (le_trans (M.sound hm).2 hb.2)

/-- The result is a `~`-congruence. -/
theorem congr {a a' b b' m m' : α} (ha : AntisymmRel (· ≤ ·) a a')
    (hb : AntisymmRel (· ≤ ·) b b')
    (h : M.meet a b = some m) (h' : M.meet a' b' = some m') :
    AntisymmRel (· ≤ ·) m m' :=
  ⟨M.greatest h' (le_trans (M.sound h).1 ha.1) (le_trans (M.sound h).2 hb.1),
   M.greatest h (le_trans (M.sound h').1 ha.2) (le_trans (M.sound h').2 hb.2)⟩

private theorem qmeet_respects {a a' b b' : α}
    (ha : AntisymmRel (· ≤ ·) a a') (hb : AntisymmRel (· ≤ ·) b b') :
    (M.meet a b).map cls = (M.meet a' b').map cls := by
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
    exact congrArg some (cls_eq_cls (M.congr ha hb h h'))

/-- The meet descended to `S/~`. -/
def qmeet : Q α → Q α → Option (Q α) :=
  Quotient.lift₂ (fun a b => (M.meet a b).map cls)
    (fun _ _ _ _ ha hb => M.qmeet_respects ha hb)

theorem qmeet_mk (a b : α) : M.qmeet (cls a) (cls b) = (M.meet a b).map cls :=
  rfl

/-! (M1)–(M3) descend to the quotient. -/

theorem qmeet_sound {x y m : Q α} : M.qmeet x y = some m → m ≤ x ∧ m ≤ y := by
  induction x using Q.inductionOn with
  | mk a =>
    induction y using Q.inductionOn with
    | mk b =>
      intro h
      rw [qmeet_mk] at h
      cases hab : M.meet a b with
      | none => rw [hab] at h; cases h
      | some m₀ =>
        rw [hab] at h
        obtain rfl := Option.some.inj h
        exact ⟨cls_le_cls.mpr (M.sound hab).1, cls_le_cls.mpr (M.sound hab).2⟩

theorem qmeet_greatest {x y m c : Q α} :
    M.qmeet x y = some m → c ≤ x → c ≤ y → c ≤ m := by
  induction x using Q.inductionOn with
  | mk a =>
    induction y using Q.inductionOn with
    | mk b =>
      induction c using Q.inductionOn with
      | mk c₀ =>
        intro h h₁ h₂
        rw [qmeet_mk] at h
        cases hab : M.meet a b with
        | none => rw [hab] at h; cases h
        | some m₀ =>
          rw [hab] at h
          obtain rfl := Option.some.inj h
          exact cls_le_cls.mpr
            (M.greatest hab (cls_le_cls.mp h₁) (cls_le_cls.mp h₂))

theorem qmeet_total {x y c : Q α} :
    c ≤ x → c ≤ y → ∃ m, M.qmeet x y = some m := by
  induction x using Q.inductionOn with
  | mk a =>
    induction y using Q.inductionOn with
    | mk b =>
      induction c using Q.inductionOn with
      | mk c₀ =>
        intro h₁ h₂
        obtain ⟨m, hm⟩ := M.total (cls_le_cls.mp h₁) (cls_le_cls.mp h₂)
        exact ⟨cls m, by rw [qmeet_mk, hm]; rfl⟩

/-! Adjoin `⊥` for "undefined" and the partial meet becomes a total one on
    `WithBot (S/~)` — the standard resolution of the doc's open question on
    admitting a bottom, in its order-theoretic form. -/

/-- The total meet on `WithBot (S/~)`: `⊥` absorbs, and an undefined
    `qmeet` is sent to `⊥`. -/
def binf : WithBot (Q α) → WithBot (Q α) → WithBot (Q α) :=
  WithBot.recBotCoe (fun _ => ⊥)
    (fun x => WithBot.recBotCoe ⊥ (fun y => (M.qmeet x y).elim ⊥ (↑·)))

@[simp] theorem binf_bot_left (y : WithBot (Q α)) : M.binf ⊥ y = ⊥ := rfl

@[simp] theorem binf_bot_right (x : WithBot (Q α)) : M.binf x ⊥ = ⊥ :=
  WithBot.recBotCoe rfl (fun _ => rfl) x

@[simp] theorem binf_coe_coe (x y : Q α) :
    M.binf x y = (M.qmeet x y).elim ⊥ (↑·) := rfl

/-- `SemilatticeInf (WithBot (S/~))` from (M1)–(M3). -/
@[instance_reducible] def semilatticeInf : SemilatticeInf (WithBot (Q α)) where
  inf := M.binf
  inf_le_left x y := by
    induction x using WithBot.recBotCoe with
    | bot => simp
    | coe a =>
      induction y using WithBot.recBotCoe with
      | bot => simp
      | coe b =>
        rw [binf_coe_coe]
        cases h : M.qmeet a b with
        | none => exact bot_le
        | some m => exact WithBot.coe_le_coe.mpr (M.qmeet_sound h).1
  inf_le_right x y := by
    induction x using WithBot.recBotCoe with
    | bot => simp
    | coe a =>
      induction y using WithBot.recBotCoe with
      | bot => simp
      | coe b =>
        rw [binf_coe_coe]
        cases h : M.qmeet a b with
        | none => exact bot_le
        | some m => exact WithBot.coe_le_coe.mpr (M.qmeet_sound h).2
  le_inf x y z hxy hxz := by
    induction x using WithBot.recBotCoe with
    | bot => exact bot_le
    | coe c =>
      induction y using WithBot.recBotCoe with
      | bot => exact absurd hxy (WithBot.not_coe_le_bot c)
      | coe a =>
        induction z using WithBot.recBotCoe with
        | bot => exact absurd hxz (WithBot.not_coe_le_bot c)
        | coe b =>
          obtain ⟨m, hm⟩ :=
            M.qmeet_total (WithBot.coe_le_coe.mp hxy) (WithBot.coe_le_coe.mp hxz)
          rw [binf_coe_coe, hm]
          exact WithBot.coe_le_coe.mpr
            (M.qmeet_greatest hm (WithBot.coe_le_coe.mp hxy) (WithBot.coe_le_coe.mp hxz))

/-- Conversely, every meet-semilattice is a `PartialMeet` with a total
    meet: (M1)–(M3) are the semilattice axioms, specialized to
    partiality. -/
def ofSemilatticeInf {γ : Type u} [SemilatticeInf γ] : PartialMeet γ where
  meet a b := some (a ⊓ b)
  sound h := by obtain rfl := Option.some.inj h; exact ⟨inf_le_left, inf_le_right⟩
  greatest h h₁ h₂ := by obtain rfl := Option.some.inj h; exact le_inf h₁ h₂
  total _ _ := ⟨_, rfl⟩

end PartialMeet

/-! The equational laws of the quotient meet, for any `SemilatticeInf` and
    hence for `WithBot (S/~)` via `PartialMeet.semilatticeInf`: -/
section

variable {γ : Type u} [SemilatticeInf γ] (x y z : γ)

example : x ⊓ x = x := inf_idem x
example : x ⊓ y = y ⊓ x := inf_comm x y
example : x ⊓ y ⊓ z = x ⊓ (y ⊓ z) := inf_assoc x y z

end

/-! ### 4. Annotations invisible to the order

A payload dimension `satisfies` does not read.  Its order is not the
product order, and the collapse of the quotients is an order
isomorphism. -/

/-- A payload with an annotation the order ignores — the propagation policy
    on an edge (`%` vs `%%`). -/
def Ann (α : Type u) (π : Type v) : Type (max u v) := α × π

instance [Preorder α] {π : Type v} : Preorder (Ann α π) where
  le x y := x.1 ≤ y.1
  le_refl x := le_refl x.1
  le_trans _ _ _ h₁ h₂ := le_trans h₁ h₂

/-- Quotienting erases the annotation: `(S × Π)/~ ≃o S/~`. -/
def annIso [Preorder α] (π : Type v) [Inhabited π] : Q (Ann α π) ≃o Q α where
  toFun := Quotient.lift (fun x : Ann α π => (cls x.1 : Q α))
    (fun _ _ h => Quotient.sound' h)
  invFun := Quotient.lift (fun a : α => (cls ((a, default) : Ann α π) : Q (Ann α π)))
    (fun _ _ h => Quotient.sound' h)
  left_inv x := by
    induction x using Q.inductionOn with
    | mk a => exact cls_eq_cls (α := Ann α π) ⟨le_refl a.1, le_refl a.1⟩
  right_inv y := by
    induction y using Q.inductionOn with
    | mk a => rfl
  map_rel_iff' {x y} := by
    induction x using Q.inductionOn with
    | mk a =>
      induction y using Q.inductionOn with
      | mk b => exact cls_le_cls.trans cls_le_cls.symm

/-! ### 5. Products

A node compares componentwise — the `Prod` order instance — and
`constrain` merges dimension by dimension. -/

example [Preorder α] [Preorder β] (a₁ a₂ : α) (b₁ b₂ : β) :
    ((a₁, b₁) : α × β) ≤ (a₂, b₂) ↔ a₁ ≤ a₂ ∧ b₁ ≤ b₂ :=
  Prod.mk_le_mk

/-- `constrain` merges dimension by dimension and fails if any dimension is
    disjoint. -/
def PartialMeet.prod [Preorder α] [Preorder β] (M : PartialMeet α) (N : PartialMeet β) :
    PartialMeet (α × β) where
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

/-! #### Flat domains with an unconstrained top —

`Flat α` is `WithTop` of the discrete order on `α`, defined directly
(Mathlib has no discrete-order instance).  `none` is the absent
constraint, `some x` pins the value. -/

def Flat (α : Type u) : Type u := Option α

instance : Preorder (Flat α) where
  le x y := y = none ∨ x = y
  le_refl _ := Or.inr rfl
  le_trans a b c h₁ h₂ := by
    cases h₂ with
    | inl h => exact Or.inl h
    | inr h =>
      cases h₁ with
      | inl h' => exact Or.inl (h ▸ h')
      | inr h' => exact Or.inr (h'.trans h)

/-- `constrain` keeps the more constrained side and fails on a pinned-value
    clash. -/
def flatMeet (α : Type u) [DecidableEq α] : PartialMeet (Flat α) where
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
      cases h₁ with
      | inl h => cases h
      | inr h =>
        cases h₂ with
        | inl h' => cases h'
        | inr h' =>
          have hab : a = b := Option.some.inj (h.symm.trans h')
          exact ⟨some a, by simp [hab]⟩

/-! #### Multi-valued variant constraints

Value lists ordered by reverse membership denote finite sets: the
dimension is `(Finset α)ᵒᵈ`, the order dual of the `Finset` lattice,
whose meet (union) is total; it enters the framework through
`PartialMeet.ofSemilatticeInf`. -/

/-- `S ≤ T` iff `S` requires every value `T` does — reverse inclusion, the
    dual order. -/
example (S T : (Finset ℕ)ᵒᵈ) :
    S ≤ T ↔ OrderDual.ofDual T ⊆ OrderDual.ofDual S :=
  Iff.rfl

/-- The meet is union and never fails. -/
example : PartialMeet (Finset ℕ)ᵒᵈ := .ofSemilatticeInf

/-- Reordered, duplicated value lists denote one `Finset`. -/
example : ([1, 2] : List ℕ).toFinset = [2, 1, 1].toFinset := by decide

/-! ### 7. The dependency DAG: simulation order on rooted labelled trees -/

inductive Tree (ν : Type u) (ε : Type v) : Type (max u v) where
  | node : ν → (n : Nat) → (Fin n → ε) → (Fin n → Tree ν ε) → Tree ν ε

namespace Tree

variable {ν : Type u} {ε : Type v} [Preorder ν] [Preorder ε]

/-- The simulation order: the roots compare, and a witness map sends every
    edge of the constraint to an edge of the candidate with a satisfying
    label and a recursively satisfying child. -/
inductive TLe : Tree ν ε → Tree ν ε → Prop where
  | node {a b : ν} {n m : Nat}
      {la : Fin n → ε} {ca : Fin n → Tree ν ε}
      {lb : Fin m → ε} {cb : Fin m → Tree ν ε}
      (f : Fin m → Fin n) :
      a ≤ b →
      (∀ j, la (f j) ≤ lb j) →
      (∀ j, TLe (ca (f j)) (cb j)) →
      TLe (.node a n la ca) (.node b m lb cb)

theorem TLe.refl : ∀ t : Tree ν ε, TLe t t := by
  intro t
  induction t with
  | node a n la ca ih =>
    exact TLe.node (fun j => j) (le_refl a) (fun j => le_refl _) (fun j => ih j)

theorem TLe.trans :
    ∀ {s t u : Tree ν ε}, TLe s t → TLe t u → TLe s u := by
  intro s t u h₁ h₂
  induction h₂ generalizing s with
  | @node b c m k lb cb lc cc g hbc hlab hsub ih =>
    cases h₁ with
    | node f hab hlab' hsub' =>
      exact TLe.node (fun j => f (g j)) (le_trans hab hbc)
        (fun j => le_trans (hlab' (g j)) (hlab j))
        (fun j => ih j (hsub' (g j)))

/-- `satisfies` on dependency structures is a preorder, so the quotient
    and meet development above applies to trees. -/
instance : Preorder (Tree ν ε) where
  le := TLe
  le_refl := TLe.refl
  le_trans _ _ _ := TLe.trans

/-- Edge annotations invisible to the edge order are invisible to the tree
    order: one-edge specs differing only in the policy annotation are
    mutually satisfying. -/
example {π : Type v} (a b : ν) (e : ε) (p q : π)
    (hab : AntisymmRel (· ≤ ·) a b) (t : Tree ν (Ann ε π)) :
    AntisymmRel (α := Tree ν (Ann ε π)) (· ≤ ·)
      (.node a 1 (fun _ => ((e, p) : Ann ε π)) (fun _ => t))
      (.node b 1 (fun _ => ((e, q) : Ann ε π)) (fun _ => t)) := by
  constructor
  · show TLe _ _
    exact TLe.node (fun j => j) hab.1 (fun _ => le_refl _) (fun _ => TLe.refl t)
  · show TLe _ _
    exact TLe.node (fun j => j) hab.2 (fun _ => le_refl _) (fun _ => TLe.refl t)

end Tree

/-! ### 8. The repo projection as a partial kernel operator

`substitute_abstract_variants` refines a spec against a repository and
raises outside its domain; its contract (spec-semantics.tex, rem:kernel)
makes it a *partial kernel operator*, and freezing of provided virtuals
is a second intended instance.  The four axioms are the harness laws
`pir_refines`, `pir_idempotent`, `pir_monotone` and `pir_defined_upward`;
the fifth law, `pir_meet_commutes`, is derived below from these together
with (M1)–(M3).  Totalized over `WithBot (S/~)`, the kernel is a
`ClosureOperator` on the dual order. -/

/-- A partial kernel operator: the repo projection π_R.  `proj s = none`
    models raising, reserved by contract for specs with no R-valid state
    below them.  The four axioms are, in order, the harness laws
    `pir_refines`, `pir_idempotent`, `pir_monotone`, `pir_defined_upward`. -/
structure PartialKernel (α : Type u) [Preorder α] : Type u where
  proj : α → Option α
  refines : ∀ {s p}, proj s = some p → p ≤ s
  idem : ∀ {s p}, proj s = some p → ∃ q, proj p = some q ∧ AntisymmRel (· ≤ ·) q p
  mono : ∀ {a b p q}, a ≤ b → proj a = some p → proj b = some q → p ≤ q
  defined_up : ∀ {a b p}, a ≤ b → proj a = some p → ∃ q, proj b = some q

namespace PartialKernel

variable [Preorder α] (K : PartialKernel α)

/-- A fixed point of the projection: an R-valid state. -/
def IsFixed (v : α) : Prop := ∃ w, K.proj v = some w ∧ AntisymmRel (· ≤ ·) w v

theorem isFixed_of_proj {s p : α} (h : K.proj s = some p) : K.IsFixed p :=
  K.idem h

/-- The universal property: a defined projection is the greatest fixed
    point below its argument. -/
theorem greatest {v s p : α} (hv : K.IsFixed v) (hvs : v ≤ s)
    (hp : K.proj s = some p) : v ≤ p := by
  obtain ⟨w, hw, hwv⟩ := hv
  exact le_trans hwv.2 (K.mono hvs hw hp)

/-- The adjunction law with the fixed points: for an R-valid `v`,
    `v ≤ π(s)` iff `v ≤ s` — the projection is invisible to every R-valid
    observer. -/
theorem le_proj_iff {v s p : α} (hv : K.IsFixed v) (hp : K.proj s = some p) :
    v ≤ p ↔ v ≤ s :=
  ⟨fun h => le_trans h (K.refines hp), fun h => K.greatest hv h hp⟩

section Commutation

variable (M : PartialMeet α)

/-- Half of the harness law `pir_meet_commutes`: where `π(a ∧ b)` is
    defined, the re-projected right-hand side `π(π(a) ∧ π(b))` is defined
    and equivalent, from the four kernel axioms and (M1)–(M3). -/
theorem meet_commutes_forward {a b ab k : α}
    (hab : M.meet a b = some ab) (hk : K.proj ab = some k) :
    ∃ pa pb pm k',
      K.proj a = some pa ∧ K.proj b = some pb ∧ M.meet pa pb = some pm ∧
        K.proj pm = some k' ∧ AntisymmRel (· ≤ ·) k k' := by
  obtain ⟨hab_a, hab_b⟩ := M.sound hab
  obtain ⟨pa, hpa⟩ := K.defined_up hab_a hk
  obtain ⟨pb, hpb⟩ := K.defined_up hab_b hk
  have hk_pa : k ≤ pa := K.mono hab_a hk hpa
  have hk_pb : k ≤ pb := K.mono hab_b hk hpb
  obtain ⟨pm, hpm⟩ := M.total hk_pa hk_pb
  have hk_pm : k ≤ pm := M.greatest hpm hk_pa hk_pb
  obtain ⟨w, hw, hwk⟩ := K.idem hk
  obtain ⟨k', hk'⟩ := K.defined_up hk_pm hw
  refine ⟨pa, pb, pm, k', hpa, hpb, hpm, hk', ?_, ?_⟩
  · exact K.greatest (K.isFixed_of_proj hk) hk_pm hk'
  · have hk'_pm : k' ≤ pm := K.refines hk'
    have hk'_a : k' ≤ a := le_trans hk'_pm (le_trans (M.sound hpm).1 (K.refines hpa))
    have hk'_b : k' ≤ b := le_trans hk'_pm (le_trans (M.sound hpm).2 (K.refines hpb))
    exact K.greatest (K.isFixed_of_proj hk') (M.greatest hab hk'_a hk'_b) hk

/-- The other half: where the re-projected right-hand side is defined,
    `π(a ∧ b)` is defined and equivalent.  Together with the forward half
    this is the definedness-iff of the harness law. -/
theorem meet_commutes_backward {a b pa pb pm k' : α}
    (hpa : K.proj a = some pa) (hpb : K.proj b = some pb)
    (hpm : M.meet pa pb = some pm) (hk' : K.proj pm = some k') :
    ∃ ab k, M.meet a b = some ab ∧ K.proj ab = some k ∧
      AntisymmRel (· ≤ ·) k k' := by
  have hk'_pm : k' ≤ pm := K.refines hk'
  have hk'_a : k' ≤ a := le_trans hk'_pm (le_trans (M.sound hpm).1 (K.refines hpa))
  have hk'_b : k' ≤ b := le_trans hk'_pm (le_trans (M.sound hpm).2 (K.refines hpb))
  obtain ⟨ab, hab⟩ := M.total hk'_a hk'_b
  have hk'_ab : k' ≤ ab := M.greatest hab hk'_a hk'_b
  obtain ⟨w, hw, hwk'⟩ := K.idem hk'
  obtain ⟨k, hk⟩ := K.defined_up hk'_ab hw
  refine ⟨ab, k, hab, hk, ?_, ?_⟩
  · have hk_pa : k ≤ pa := K.mono (M.sound hab).1 hk hpa
    have hk_pb : k ≤ pb := K.mono (M.sound hab).2 hk hpb
    exact K.greatest (K.isFixed_of_proj hk) (M.greatest hpm hk_pa hk_pb) hk'
  · exact K.greatest (K.isFixed_of_proj hk') hk'_ab hk

end Commutation

/-! Descending to the quotient and totalizing with `⊥`, as for the meet,
    turns the partial kernel into a `ClosureOperator` on the dual
    order. -/

theorem congr_def {a a' : α} (ha : AntisymmRel (· ≤ ·) a a') :
    (∃ p, K.proj a = some p) ↔ (∃ p, K.proj a' = some p) :=
  ⟨fun ⟨_p, hp⟩ => K.defined_up ha.1 hp, fun ⟨_p, hp⟩ => K.defined_up ha.2 hp⟩

theorem congr {a a' p p' : α} (ha : AntisymmRel (· ≤ ·) a a')
    (h : K.proj a = some p) (h' : K.proj a' = some p') :
    AntisymmRel (· ≤ ·) p p' :=
  ⟨K.mono ha.1 h h', K.mono ha.2 h' h⟩

private theorem qproj_respects {a a' : α} (ha : AntisymmRel (· ≤ ·) a a') :
    (K.proj a).map cls = (K.proj a').map cls := by
  cases h : K.proj a with
  | none =>
    cases h' : K.proj a' with
    | none => rfl
    | some p' =>
      obtain ⟨p, hp⟩ := (K.congr_def ha).mpr ⟨p', h'⟩
      rw [h] at hp
      cases hp
  | some p =>
    obtain ⟨p', h'⟩ := (K.congr_def ha).mp ⟨p, h⟩
    rw [h']
    exact congrArg some (cls_eq_cls (K.congr ha h h'))

/-- The projection descended to `S/~`. -/
def qproj : Q α → Option (Q α) :=
  Quotient.lift (fun a => (K.proj a).map cls) (fun _ _ h => K.qproj_respects h)

theorem qproj_mk (a : α) : K.qproj (cls a) = (K.proj a).map cls :=
  rfl

theorem qproj_refines {x p : Q α} : K.qproj x = some p → p ≤ x := by
  induction x using Q.inductionOn with
  | mk a =>
    intro h
    rw [qproj_mk] at h
    cases ha : K.proj a with
    | none => rw [ha] at h; cases h
    | some p₀ =>
      rw [ha] at h
      obtain rfl := Option.some.inj h
      exact cls_le_cls.mpr (K.refines ha)

theorem qproj_mono_defined {x y p : Q α} :
    x ≤ y → K.qproj x = some p → ∃ q, K.qproj y = some q ∧ p ≤ q := by
  induction x using Q.inductionOn with
  | mk a =>
    induction y using Q.inductionOn with
    | mk b =>
      intro hxy h
      rw [qproj_mk] at h
      cases ha : K.proj a with
      | none => rw [ha] at h; cases h
      | some p₀ =>
        rw [ha] at h
        obtain rfl := Option.some.inj h
        obtain ⟨q₀, hq⟩ := K.defined_up (cls_le_cls.mp hxy) ha
        exact ⟨cls q₀, by rw [qproj_mk, hq]; rfl,
          cls_le_cls.mpr (K.mono (cls_le_cls.mp hxy) ha hq)⟩

/-- On the quotient, idempotence is an equality. -/
theorem qproj_idem {x p : Q α} : K.qproj x = some p → K.qproj p = some p := by
  induction x using Q.inductionOn with
  | mk a =>
    intro h
    rw [qproj_mk] at h
    cases ha : K.proj a with
    | none => rw [ha] at h; cases h
    | some p₀ =>
      rw [ha] at h
      obtain rfl := Option.some.inj h
      obtain ⟨q₀, hq, hqp⟩ := K.idem ha
      rw [qproj_mk, hq]
      exact congrArg some (cls_eq_cls hqp)

/-- The totalization: `⊥` for out-of-domain, as for the meet.  Upward-closed
    definedness is exactly what makes it monotone. -/
def kbot : WithBot (Q α) → WithBot (Q α) :=
  WithBot.recBotCoe ⊥ (fun x => (K.qproj x).elim ⊥ (↑·))

@[simp] theorem kbot_bot : K.kbot ⊥ = ⊥ := rfl

@[simp] theorem kbot_coe (x : Q α) : K.kbot x = (K.qproj x).elim ⊥ (↑·) := rfl

theorem kbot_le (x : WithBot (Q α)) : K.kbot x ≤ x := by
  induction x using WithBot.recBotCoe with
  | bot => simp
  | coe a =>
    rw [kbot_coe]
    cases h : K.qproj a with
    | none => exact bot_le
    | some p => exact WithBot.coe_le_coe.mpr (K.qproj_refines h)

theorem kbot_mono : Monotone K.kbot := by
  intro x y hxy
  induction x using WithBot.recBotCoe with
  | bot => simp
  | coe a =>
    induction y using WithBot.recBotCoe with
    | bot => exact absurd hxy (WithBot.not_coe_le_bot a)
    | coe b =>
      rw [kbot_coe, kbot_coe]
      cases h : K.qproj a with
      | none => exact bot_le
      | some p =>
        obtain ⟨q, hq, hpq⟩ := K.qproj_mono_defined (WithBot.coe_le_coe.mp hxy) h
        rw [hq]
        exact WithBot.coe_le_coe.mpr hpq

theorem kbot_idem (x : WithBot (Q α)) : K.kbot (K.kbot x) = K.kbot x := by
  induction x using WithBot.recBotCoe with
  | bot => simp
  | coe a =>
    rw [kbot_coe]
    cases h : K.qproj a with
    | none => simp
    | some p =>
      show K.kbot (p : WithBot (Q α)) = (p : WithBot (Q α))
      rw [kbot_coe, K.qproj_idem h]
      rfl

/-- The totalized kernel as a `ClosureOperator` on the dual order, where
    deflationary reads as inflationary.  Its closed elements are the
    R-valid states. -/
def closureOperator : ClosureOperator (WithBot (Q α))ᵒᵈ where
  toFun x := OrderDual.toDual (K.kbot (OrderDual.ofDual x))
  monotone' _ _ h := K.kbot_mono h
  le_closure' x := K.kbot_le (OrderDual.ofDual x)
  idempotent' x := congrArg OrderDual.toDual (K.kbot_idem (OrderDual.ofDual x))

/-- The Galois insertion with the closed elements — on the kernel side, the
    coinsertion between specs and R-valid states. -/
example : GaloisInsertion K.closureOperator.toCloseds (↑·) :=
  K.closureOperator.gi

end PartialKernel

end SpecSemantics
