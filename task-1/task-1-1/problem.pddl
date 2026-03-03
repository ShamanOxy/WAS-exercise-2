(define (problem scheduling-problem)
  (:domain maintenance-scheduling)
  
  (:objects
    inhabitant1 inhabitant2 inhabitant3 - inhabitant
    room1 room2 room3 - room
    am9 am915 am10 am1015 am11 - time
  )
  
  (:init
    ; Room assignments
    (assigned-room inhabitant1 room1)
    (assigned-room inhabitant2 room2)
    (assigned-room inhabitant3 room3)
    
    ; Available arrival times for each inhabitant
    (can-arrive inhabitant1 am9)
    (can-arrive inhabitant1 am915)
    (can-arrive inhabitant2 am9)
    (can-arrive inhabitant3 am10)
    (can-arrive inhabitant3 am1015)
    
    ; Worker is initially available at all times
    (worker-available am9)
    (worker-available am915)
    (worker-available am10)
    (worker-available am1015)
    (worker-available am11)
  )
  
  (:goal (and
    (scheduled inhabitant1)
    (scheduled inhabitant2)
    (scheduled inhabitant3)
  ))
)
