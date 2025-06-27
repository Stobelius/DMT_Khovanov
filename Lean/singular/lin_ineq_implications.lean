import Mathlib.Algebra.Order.Ring.Star
import Mathlib.Analysis.Normed.Field.Lemmas
import Mathlib.Data.Rat.Star

def tA (n : ℚ) (h q : ℚ) : ℚ := (-1/2) * n + 1/2 * h - 1/4 * q - 1
def tB (n : ℚ) (h q : ℚ) : ℚ := 3 * n - 3/2 * h + q - 5/2
def tC (n : ℚ) (h q : ℚ) : ℚ := (-9/4) * n + h - 3/4 * q - 1/4

lemma lemma_6_2_case_two (n : ℚ) (h₁ h₂ q₁ q₂ : ℚ)
    (htA₁ : (-3/2) ≤ tA n h₁ q₁) (htA₁' : tA n h₁ q₁ < 2)
    (htC₁ : (-3/2) ≤ tC n h₁ q₁)
    (htA₂ : (-3/2) ≤ tA n h₂ q₂)
    (htC₂ : (-3/2) ≤ tC n h₂ q₂) (htC₂' : tC n h₂ q₂ < 2)
    (hh : h₁ + 1 = h₂) (hn : 83 ≤ n) :
    2 ≤ tB n h₁ q₁ := by
  rw [tA, tB, tC] at *
  linarith

lemma lemma_6_2_case_two' (n : ℚ) (h₁ h₂ q₁ q₂ : ℚ)
    (htA₁ : (-3/2) ≤ tA n h₁ q₁) (htA₁' : tA n h₁ q₁ < 2)
    (htC₁ : (-3/2) ≤ tC n h₁ q₁)
    (htA₂ : (-3/2) ≤ tA n h₂ q₂)
    (htC₂ : (-3/2) ≤ tC n h₂ q₂) (htC₂' : tC n h₂ q₂ < 2)
    (hh : h₁ + 1 = h₂) (hn : 83 ≤ n):
    2 ≤ tB n h₂ q₂ := by
  rw [tA, tB, tC] at *
  linarith

lemma corollary_4_2 (n h q : ℚ)
    (htA : tA n h q < 2)
    (htB : tB n h q < 2)
    (htC : tC n h q < 2):
    n <39:= by
  rw [tA, tB, tC] at *
  linarith

--Proof of Theorem 1.2
--the functions f and g appear in both Proposition 4.6 and Theorem 1.1

def f (n i j : ℚ) : ℚ := -9*n+4*i-3*j

def g (n i j : ℚ) : ℚ := -2*n+2*i-j

/-
We use the following variables:
n  - this is the n which appers in the captions
t  - number of twists. Possible values for t: n, 2n, 2n+1, 4n, 4n+2
i  - homological degree
j  - quantum degree

With the first isomorphism of Theorem 1.1, we pull Kh^{i,j}(T(4,-t))
from Kh^{i,j+12}(T(4,-(t-4))) where
This is possible when g(t-4,i,j+12) ≥ 14.

With the second isomorphism of Theorem 1.1, we pull Kh^{i,j}(T(4,-t))
from Kh^{i+8,j+24}(T(4,-(t-4)))
This is possible when f(t-4,i+8,j+24) ≥ 41.

Otherwise we show that the group vanishes when
g(t,i,j) < -6 or f(t,i,j) < -17

For t≥ 83 we show that every group displayed in Figures 1, 17, 18
either one of the isomorphisms theorems or one of the vasnishing result applies.
-/

-- HIGHEST DEGREES: Figure 17

-- For every i,j with i≥ -41 either first recursion result or second vanishing result applies
lemma theorem_1_2_highest_either (n i j t: ℚ)
    (Hₜ : t≥ 83)(H₁ : t=n) (H₂ : i≥ -41):
    (g (t-4) i (j+12) ≥ 14) ∨ (f t i j < -17):= by
    by_cases P : g (t-4) i (j+12)  ≥ 14
    · left
      exact P
    · right
      rw [f] at *
      rw [g] at P
      linarith
-- For every nontrivial group with i≥ -41 the first recursion result applies.
-- The nontrivial group with lowest g value is at hdeg -40 and qdeg -3n-50
lemma theorem_1_2_highest_nontrivials (n i j t: ℚ)
    (Hₜ : t≥ 83)(H₁ : t=n) (H₂ : i≥ -41)(H₃ : i=-40)(H₄ : j=-3*n-50):
    (g (t-4) i (j+12) ≥ 14):= by
    rw [g]
    linarith

-- MIDDLE DEGREES: Figure 1
-- t even: t = 2n

-- in -49 ≤ i ≤ -42 the first recursion result applies
lemma theorem_1_2_t_even_middle_i_highest (n i j t: ℚ)
    (Hₜ : t≥ 83) (H₁ : t= 2*n)(H₂ : -49 ≤ i) (H₃ : i ≤ -42)(H₄ : j≤ (3/2)*i-6*n+5) :
    (g (t-4) i (j+12) ≥ 14):= by
    rw [g]
    linarith
-- in -4n+19 ≤ i ≤ -50 either of two recursion results apply
lemma theorem_1_2_t_even_middle_i_middle (n i j t: ℚ)
    (Hₜ : t≥ 83) (H₁ : t= 2*n)(H₂ : -4*n+19 ≤ i) (H₃ : i ≤ -50)(H₄ : j≤ (3/2)*i-6*n+5) :
    (g (t-4) i (j+12) ≥ 14) ∨ (f (t-4) (i+8) (j+24)) ≥ 41 := by
    by_cases P : g (t-4) i (j+12)  ≥ 14
    · left
      exact P
    · right
      rw [f] at *
      rw [g] at P
      linarith
-- in -4n+11 ≤ i ≤ --4n+18 the first recursion result applies
lemma theorem_1_2_t_even_middle_i_lowest (n i j t: ℚ)
    (Hₜ : t≥ 83) (H₁ : t= 2*n)(H₂ : -4*n+11 ≤ i) (H₃ : i ≤ -4*n+18)(H₄ : j≤ (3/2)*i-6*n+5) :
    (f (t-4) (i+8) (j+24)) ≥ 41:= by
    rw [f]
    linarith

-- t odd: t = 2n +1

-- in -49 ≤ i ≤ -42 the first recursion result applies
lemma theorem_1_2_t_odd_middle_i_highest (n i j t: ℚ)
    (Hₜ : t≥ 83) (H₁ : t= 2*n+1)(H₂ : -49 ≤ i) (H₃ : i ≤ -42)(H₄ : j≤ (3/2)*i-6*n+2) :
    (g (t-4) i (j+12) ≥ 14):= by
    rw [g]
    linarith
-- in -4n+15 ≤ i ≤ -50 either of two recursion results apply
lemma theorem_1_2_t_odd_middle_i_middle (n i j t: ℚ)
    (Hₜ : t≥ 83) (H₁ : t= 2*n+1)(H₂ : -4*n+15 ≤ i) (H₃ : i ≤ -50)(H₄ : j≤ (3/2)*i-6*n+2) :
    (g (t-4) i (j+12) ≥ 14) ∨ (f (t-4) (i+8) (j+24)) ≥ 41 := by
    by_cases P : g (t-4) i (j+12)  ≥ 14
    · left
      exact P
    · right
      rw [f] at *
      rw [g] at P
      linarith
-- in -4n+7 ≤ i ≤ --4n+14 the first recursion result applies
lemma theorem_1_2_t_odd_middle_i_lowest (n i j t: ℚ)
    (Hₜ : t≥ 83) (H₁ : t= 2*n+1)(H₂ : -4*n+7 ≤ i) (H₃ : i ≤ -4*n+14)(H₄ : j≤ (3/2)*i-6*n+2) :
    (f (t-4) (i+8) (j+24)) ≥ 41:= by
    rw [f]
    linarith

-- LOWEST DEGREES: Figure 18
-- t is 0 mod 4: t = 4n

-- For every i,j with i ≤  -8n + 10 either the second recursion result or the first vanishing result applies.
lemma theorem_1_2_t0_i_lowest_either (n i j t: ℚ)
    (Hₜ : t≥ 83) (H₁ : t= 4*n)(H₂ : i ≤ -8*n+10):
    (f (t-4) (i+8) (j+24) ≥ 41) ∨ g t i j < -6:= by
    by_cases P : g t i j  < -6
    · right
      exact P
    · left
      rw [f] at *
      rw [g] at P
      linarith
-- For every nontrivial group with i ≤  -8n + 10 the second recursion result applies.
-- The nontrivial group with lowest f value is at hdeg -8n+10 and qdeg -24n+24
lemma theorem_1_2_t0_i_lowest_nontrivials (n i j t: ℚ)
    (Hₜ : t≥ 83) (H₁ : t= 4*n)(H₂ : i ≤ -8*n+10)(H₃ : i = -8*n+10) (H₄: j=-24*n+24):
    f (t-4) (i+8) (j+24) ≥ 41:= by
    rewrite [f]
    linarith

-- t is 2 mod 4: t = 4n+2

-- For every i,j with i ≤  -8n + 6 either the second recursion result or the first vanishing result applies.
lemma theorem_1_2_t2_i_lowest_either (n i j t: ℚ)
    (Hₜ : t≥ 83) (H₁ : t= 4*n+2)(H₂ : i ≤ -8*n+6):
    (f (t-4) (i+8) (j+24) ≥ 41) ∨ g t i j < -6:= by
    by_cases P : g t i j  < -6
    · right
      exact P
    · left
      rw [f] at *
      rw [g] at P
      linarith
-- For every nontrivial group with i ≤  -8n + 6 the second recursion result applies.
-- The nontrivial group with lowest f value is at hdeg -8n+6 and qdeg -24n+10
lemma theorem_1_2_t2_i_lowest_nontrivials (n i j t: ℚ)
    (Hₜ : t≥ 83) (H₁ : t= 4*n+2)(H₂ : i ≤ -8*n+6)(H₃ : i = -8*n+6) (H₄: j=-24*n+10):
    f (t-4) (i+8) (j+24) ≥ 41:= by
    rewrite [f]
    linarith

-- t is 1 mod 2: t = 2n+1

-- For every i,j with i ≤  -8n + 6 either the second recursion result or the first vanishing result applies.
lemma theorem_1_2_t1_i_lowest_either (n i j t: ℚ)
    (Hₜ : t≥ 83) (H₁ : t= 2*n+1)(H₂ : i ≤ -4*n+6):
    (f (t-4) (i+8) (j+24) ≥ 41) ∨ g t i j < -6:= by
    by_cases P : g t i j  < -6
    · right
      exact P
    · left
      rw [f] at *
      rw [g] at P
      linarith
-- For every nontrivial group with i ≤  -4n + 6 the second recursion result applies.
-- The nontrivial group with lowest f value is at hdeg -4n+6 and qdeg -12n+13
lemma theorem_1_2_t1_i_lowest_nontrivials (n i j t: ℚ)
    (Hₜ : t≥ 83) (H₁ : t= 2*n+1)(H₂ : i ≤ -4*n+6)(H₃ : i = -4*n+6) (H₄: j=-12*n+13):
    f (t-4) (i+8) (j+24) ≥ 41:= by
    rewrite [f]
    linarith
