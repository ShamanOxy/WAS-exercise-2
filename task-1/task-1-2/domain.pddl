(define (domain maintenance-scheduling-extended)
  (:requirements :strips :typing)
  
  (:types
    inhabitant room time
  )
  
  (:predicates
    (can-arrive ?i - inhabitant ?t - time)
    (assigned-room ?i - inhabitant ?r - room)
    (scheduled ?i - inhabitant)
    (worker-available ?t - time)
    (unlocked ?r - room ?t - time)
    (at-room ?r - room ?t - time)
  )
  
  ; first unlock the room
  (:action unlock
    :parameters (?r - room ?t - time)
    :precondition (and
      (worker-available ?t)
    )
    :effect (and
      (unlocked ?r ?t)
    )
  )
  
  ; then join/enter the room
  (:action join
    :parameters (?r - room ?t - time)
    :precondition (and
      (unlocked ?r ?t)
      (worker-available ?t)
    )
    :effect (and
      (at-room ?r ?t)
    )
  )
  
  ; finally show the room to the inhabitant
  (:action showRoom
    :parameters (?i - inhabitant ?r - room ?t - time)
    :precondition (and
      (can-arrive ?i ?t)
      (assigned-room ?i ?r)
      (at-room ?r ?t)  ; need to be at the room first
      (worker-available ?t)
    )
    :effect (and
      (scheduled ?i)
      (not (worker-available ?t))
    )
  )
)
