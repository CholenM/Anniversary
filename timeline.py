"""
The timeline: which photo, when, and what it says.

Order is chronological. Dated photos use their EXIF date; undated ones are
placed where the visual content puts them and labelled honestly as undated
rather than given a made-up date.

`mods` tweaks how a photo is framed on the page:
  "small"      - low-res source, don't blow it up to full width
  "screenshot" - phone screenshot, give it a device-ish frame
  "wide"       - landscape shot, full-bleed
"""

CHAPTERS = [
    {
        "file": "photos/img_5516-1.jpg",
        "stamp": "Before us",
        "sub": "April 2014 · eleven years early",
        "caption": "You were already you — a lab coat, a lanyard, and no idea where any of this was heading.",
        "mods": "small",
    },
    {
        "file": "photos/img_5710-1.jpg",
        "stamp": "April 22, 2025",
        "sub": "Where it starts",
        "caption": "You tried on every pair in that shop and made me choose. I chose the one you were already wearing.",
    },
    {
        "file": "photos/img_0122-1.jpg",
        "stamp": "April 28, 2025",
        "sub": "The golden hallway",
        "caption": "You leaned your head on my shoulder like it was the most natural thing in the world. It was.",
    },
    {
        "file": "photos/img_0274-1.jpg",
        "stamp": "May 29, 2025",
        "sub": "Things we did not need",
        "caption": "A twenty-something store, nothing on the list, and one plush you refused to put down.",
    },
    {
        "file": "photos/img_3010.jpg",
        "stamp": "June 9, 2025",
        "sub": "Screenshot of a story",
        "caption": "You posted it and I screenshotted it before it could disappear. Still my favourite thing on my phone.",
        "mods": "screenshot",
    },
    {
        "file": "photos/img_3460-1.jpg",
        "stamp": "July 4, 2025",
        "sub": "Matching lanyards",
        "caption": "One table, one evening, and you still leaned into me like we were the only two people in the room.",
    },
    {
        "file": "photos/img_3674.jpg",
        "stamp": "November 19, 2025",
        "sub": "In between all the work",
        "caption": "Right in the middle of everything we had to do, you let me hold you in the hallway. Quietly. In front of everyone.",
    },
    {
        "file": "photos/attzbk4kn5ftonau09-tisvbulaqdeduvoxnc8p5kt3sso.jpg",
        "stamp": "Late 2025",
        "sub": "The team",
        "caption": "Our loud, messy, ridiculous team. You and me somewhere in the middle of them — exactly where we belong.",
    },
    {
        "file": "photos/messenger_creation_c15819a6-deca-482b-9de3-74c2b37f10f2-1.jpg",
        "stamp": "Late 2025",
        "sub": "Before I could",
        "caption": "You put the helmet on my head before I reached for it. You take care of me like it's the most natural thing you do.",
    },
    {
        "file": "photos/img_1237-1.jpg",
        "stamp": "Sometime in 2025",
        "sub": "Date unknown",
        "caption": "The wind took your hair, the sun took the picture, and you looked perfect anyway.",
    },
    {
        "file": "photos/img_6456.jpg",
        "stamp": "December 13, 2025",
        "sub": "Dinner",
        "caption": "You, a table full of food, and that exact look you get right before the first bite.",
    },
    {
        "file": "photos/attguzy0fsyqanhv9_cra_xggj9bftvlvd7ff7mjnzu6t4-1.jpg",
        "stamp": "A night, date unknown",
        "sub": "Out somewhere",
        "caption": "Some night I can't pin to the calendar. You, in that dress, and the whole room going quiet.",
    },
    {
        "file": "photos/attarlkyr59xkpqtmliksbabnjfl0asnz470gqcj5r01so-1.jpg",
        "stamp": "A night, date unknown",
        "sub": "Just for you",
        "caption": "The light, the dress, the way you looked straight into the camera. This one is only on this page.",
    },
    {
        "file": "photos/img_8123-1.jpg",
        "stamp": "April 15, 2026",
        "sub": "That lantern",
        "caption": "That orange lantern, that red top, and you pretending for one second that you weren't posing.",
    },
    {
        "file": "photos/img_8953-1.jpg",
        "stamp": "June 28, 2026",
        "sub": "At home",
        "caption": "No lanyards. No events. Just you, at home, holding on. This is the one I keep coming back to.",
        "mods": "wide",
    },
    {
        "file": "photos/img_9467.jpg",
        "stamp": "August 29, 2026",
        "sub": "Fluffy love",
        "caption": "You held that fox like you were already planning our future.",
    },
    {
        "file": "photos/img_9039.jpg",
        "stamp": "August 29, 2026",
        "sub": "Same day, same mall",
        "caption": "You made that face. I gave you a thumbs up anyway.",
    },
]

HERO = {
    "title": "To My Babyyyy",
    "name": "Andria",
    "lede": "Every photo I kept, in the order they happened.",
}

CLOSING = {
    "title": "It's us against the world",
    "body": "Every lanyard, every late event, every corridor and every dinner in between — "
            "that was always the whole point. Not the places. Us.",
    "sign": "Always, Andria.",
}