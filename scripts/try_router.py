"""Run a few example emails through the router using the real Gemini API.

Run it from the project root:
    .venv/Scripts/python scripts/try_router.py
"""

from hostel_agent.router import OWNER_EMAIL, Email, route_email

examples = [
    Email(
        sender="partners_2@tripmakery.com",
        subject="New group request (28p. | id: b8jPoHl80m7N)",
        body="""
New group request from tripmakery.com for 28 people
Create offer
 
Decline request
Hello Saint James Backpackers,

Your hotel was explicitly chosen by our customer and we would really appreciate to receive an offer from you. Please use the buttons shown above to create the offer or to reject this request in order to be able to guarantee a quick processing.

Request details
 

Group size

 
4 adults + 24 children

Travel date

 
24/05/2027 - 27/05/2027 (3 nights)

Rooms

 
2xtwin room, 1x3-bed-room, 1x4-bed-room, 1x5-bed-room, 2x6-bed-room

Children rooms

 
indifferent

Budget per person/night

 
£47 person/night

Budget per double room

 
£95 / night

Budget total

 
£3,973 total

Budget includes

 
Rooms, Board

Board

 
half board (or just breakfast)

Nationality

 
Finland

Group type

 
School

Customer language

 
General_Language

Average age (students)

 
16 - 18 y

Commission

 
10% included

tripmakery id

 
b8jPoHl80m7N

Your accommodation was explicitly selected by the customer!

 
Is the request not relevant?
Take advantage of the option to set your own filters and control which requests end up in your inbox. You can narrow down by budget, group size, room types, meeting room, etc.:


Filter requests
Quick reminder
As usual, we will automatically forward your offer to the group and will charge a commission of 10% if it is successfully booked, so make sure to include the commission in the final price for the customer.

As soon as we receive feedback from the group, we will contact you immediately so that you can process the booking.

If you have any questions about the process, you can contact us at any time! Feel free to ask about the possibility of a connection via your channel manager: This reduces the effort and increases your conversion considerably.


Thank you for cooperating with us!
Best regards from Vienna

Monika Ebner
Head of Group Management
+49 30 568 378 57
        """,
    ),
    Email(
        sender=OWNER_EMAIL,
        subject="Re: 30-Person Youth Rugby Group Accommodation – March 18–22, 2027",
        body="""
8 bed & 6 bed Dorms: £30 per person per night
4 bed dorms: £45 per night
Triple Bunk: £120 per room per night
Non en-suites: £120 per room per night
En-suites: £140 per room per night
        """,
    )
]

for email in examples:
    decision = route_email(email)  # one Gemini call per email
    print(f"Subject: {email.subject}")
    print(f"  Route:  {decision.route}")
    print(f"  Reason: {decision.reason}")
    print()
