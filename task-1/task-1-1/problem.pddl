; =============================================================================
; EXAMPLE PROBLEM — Vogt's Career Path to Real Madrid (PDDL 1.2)
; This is a simple example to help you get started. Replace it with your own
; problem for Task 1.1 (maintenance worker scheduling).
; =============================================================================
;
; Alessandro Vogt starts at FC St. Gallen at age 22. He must climb the
; European club hierarchy and arrive at Real Madrid by age 29 (7 seasons).
;
; Club hierarchy (Bundesliga + Arsenal + Leeds):
;
; Upgrade transfers require proving at the source club first.
; Lateral transfers (sideways/down moves) do not require proving.
;
; Season budget: 7 seasons (age 22→29)


(define (problem vogt-career)
  (:domain football-career)

  (:objects
    vogt - player
    st-gallen augsburg hoffenheim leipzig dortmund bayern leeds arsenal real-madrid - club
    age22 age23 age24 age25 age26 age27 age28 - age
  )

  (:init
    ; Vogt starts at St. Gallen, age 22, already proven at St. Gallen
    (at vogt st-gallen)
    (played-at vogt st-gallen)
    (proven vogt st-gallen)
    (age-of vogt age22)

    ; Age progression
    (next-age age22 age23)
    (next-age age23 age24)
    (next-age age24 age25)
    (next-age age25 age26)
    (next-age age26 age27)
    (next-age age27 age28)
    (next-age age28 age29)

    ; === Upgrade transfers (require proving at the source club) ===

    ; From St. Gallen
    (can-upgrade-transfer st-gallen hoffenheim)
    (can-lateral-transfer st-gallen augsburg)

    ; From Augsburg
    (can-upgrade-transfer augsburg hoffenheim)

    ; From Hoffenheim
    (can-upgrade-transfer hoffenheim dortmund)
    (can-upgrade-transfer hoffenheim leipzig)
    (can-upgrade-transfer hoffenheim leeds)

    ; From Leipzig 
    (can-upgrade-transfer leipzig dortmund)
    (can-upgrade-transfer leipzig bayern)

    ; From Dortmund
    (can-upgrade-transfer dortmund arsenal)

    ; From Leeds
    (can-upgrade-transfer leeds arsenal)

    ; From Arsenal — must prove yourself to reach Real Madrid
    (can-upgrade-transfer arsenal real-madrid)

    ; From Bayern — must prove yourself to reach Real Madrid
    (can-upgrade-transfer bayern real-madrid)

    ; === Lateral transfers (no proving required) ===

    ; From St. Gallen
    (can-lateral-transfer st-gallen augsburg)

    ; From Augsburg
    (can-upgrade-transfer augsburg leeds)

    ; From Dortmund
    (can-lateral-transfer dortmund leeds)

    ; === Clubs that require proving ===
    (needs-proving hoffenheim)
    (needs-proving augsburg)
    (needs-proving leipzig)
    (needs-proving dortmund)
    (needs-proving bayern)
    (needs-proving leeds)
    (needs-proving arsenal)
  )

  (:goal (and
    (at vogt real-madrid)
    (age-of vogt age29)
  ))
)
