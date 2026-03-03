(define (domain maintenance-scheduling)
  (:requirements :strips :typing)
  
  (:types
    inhabitant room time
  )
  
  (:predicates
    (can-arrive ?i - inhabitant ?t - time)
    (assigned-room ?i - inhabitant ?r - room)
    (scheduled ?i - inhabitant)
    (worker-available ?t - time)
  )
  
  ; action to schedule an inhabitant at a specific time
  (:action showRoom
    :parameters (?i - inhabitant ?r - room ?t - time)
    :precondition (and
      (can-arrive ?i ?t)
      (assigned-room ?i ?r)
      (worker-available ?t)
    )
    :effect (and
      (scheduled ?i)
      (not (worker-available ?t))  ; worker becomes busy at this time
    )
  )
)
