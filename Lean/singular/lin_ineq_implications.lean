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
t  - number of twists. Often t =2n +1 or similar
i  - homological degree
j  - quantum degree

With the first isomorphism of Theorem 1.1, we pull Kh^{i,j}(T(4,-t))
from Kh^{i',j'}(T(4,-t')) where
t'=t-4
i'=i
j'=j+12
This is possible when g(t',i',j') ≥ 14.

With the second isomorphism of Theorem 1.1, we pull Kh^{i,j}(T(4,-t))
from Kh^{i',j'}(T(4,-t')) where
t''=t-4
i''=i+8
j''=j+24
This is possible when f(t'',i'',j'') ≥ 41.

Otherwise we show that the group vanishes when
g(t,i,j) < -6 or f(t,i,j) < -17
-/


-- highest degrees: Figure 16


lemma theorem_1_2_highest_degrees'' (n t i j t' i' j' t'' j'' i'' : ℚ)
    (H₁ : t'=t-4) (H₂ : i'=i) (H₃ : j'=j+12)(H₄ : t''=t-4)(H₅ : i''=i+8) (H₆ : j''=j+24)(H₇ : t≥ 83)
    (h₁ : n=t) (h₂ : -41 ≤ i) (h₃ : -17 ≤ f t i j):
    ( g t' i' j'  ≥ 14):= by
    rw [f] at *
    rw [g]
    linarith

lemma theorem_1_2_highest_degrees''' (n t i j t' i' j' t'' j'' i'' : ℚ)
    (H₁ : t'=t-4) (H₂ : i'=i) (H₃ : j'=j+12)(H₄ : t''=t-4)(H₅ : i''=i+8) (H₆ : j''=j+24)(H₇ : t≥ 83)
    (h₁ : n=t) (h₂ : -41 ≤ i):
    ( (g t' i' j'  ≥ 14) ∨  (-17 > f t i j)):= by
    rw [f] at *
    rw [g]
    sorry










/-
lemma theorem_1_2_highest_degrees (n i j : ℚ)
    (h_1 : 51 ≤ n) (h_2 : -41 ≤ i) (h_3 : -17 ≤ f n i j)(h_4 : i≤ 0) (h_5 : j<=0) :
    (g (n-4) i (j+12) ≥ 14):= by
    rw [f] at *
    linarith
-/
