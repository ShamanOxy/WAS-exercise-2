; =============================================================================
; EXAMPLE DOMAIN — Football Career Path (PDDL 1.2)
; This is a simple example to help you get started. Replace it with your own
; domain for Task 1.1 (maintenance worker scheduling).
; =============================================================================
;
; A young football player progresses through clubs, ages over time.
; Clubs have a hierarchy — you can only transfer to a club if a transfer
; path exists. Some clubs require the player to prove themselves first
; (play a full season) before they can transfer out.

(define (domain football-career)
  (:requirements :strips :typing)

  (:types
    player club age
  )

  (:predicates
    (at ?p - player ?c - club)                          ; player is currently at this club
    (age-of ?p - player ?a - age)                       ; player's current age
    (next-age ?a1 - age ?a2 - age)                      ; a2 is the age after a1
    (played-at ?p - player ?c - club)                   ; player has played at this club before
    (can-upgrade-transfer ?from - club ?to - club)      ; upward transfer path (requires proving)
    (can-lateral-transfer ?from - club ?to - club)      ; lateral/down transfer path (no proving needed)
    (proven ?p - player ?c - club)                      ; player has proven themselves at this club
    (needs-proving ?c - club)                           ; this club requires proving before transfer out
  )

  ; Play a season at current club to prove yourself (required at some clubs)
  (:action play-season
    :parameters (?p - player ?c - club ?a1 - age ?a2 - age)
    :precondition (and
      (at ?p ?c)
      (age-of ?p ?a1)
      (next-age ?a1 ?a2)
    )
    :effect (and
      (proven ?p ?c)
      (age-of ?p ?a2)
      (not (age-of ?p ?a1))
    )
  )

  ; Upgrade transfer — move up to a bigger club (must be proven first)
  (:action upgrade-transfer
    :parameters (?p - player ?from - club ?to - club ?a1 - age ?a2 - age)
    :precondition (and
      (at ?p ?from)
      (can-upgrade-transfer ?from ?to)
      (proven ?p ?from)
      (age-of ?p ?a1)
      (next-age ?a1 ?a2)
    )
    :effect (and
      (at ?p ?to)
      (played-at ?p ?to)
      (age-of ?p ?a2)
      (not (at ?p ?from))
      (not (age-of ?p ?a1))
    )
  )

  ; Lateral transfer — sideways or downward move (no proving required)
  (:action lateral-transfer
    :parameters (?p - player ?from - club ?to - club ?a1 - age ?a2 - age)
    :precondition (and
      (at ?p ?from)
      (can-lateral-transfer ?from ?to)
      (age-of ?p ?a1)
      (next-age ?a1 ?a2)
    )
    :effect (and
      (at ?p ?to)
      (played-at ?p ?to)
      (age-of ?p ?a2)
      (not (at ?p ?from))
      (not (age-of ?p ?a1))
    )
  )
)
