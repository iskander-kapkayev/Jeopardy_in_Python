# Question Data Structure: Category -> [(Question, Answer, Points, ...)]
def define_questions():
    jeopardy_questions = {
        "Star Wars?!": [
            ("This is the name of Han Solo's ship. He probably got tons of putang.", "falcon", 100),
            ("This planet is the home to Wicket and the Ewoks", "endor", 200),
            ("This is the composer of all star wars music", "john williams", 300),
            ("Living a long time is part of Yoda's schtick - he was estimated to be this old when he died", "900", 400),
            ("This actor plays both an important member of the jedi and a character in the MCU", "jackson", 500),
        ],
        "Anime Quotes": [
            ("My grandfather’s deck has no pathetic cards!", "Yugi", 200),
            ("If you don't take risks, you can't create a future.", "Luffy", 400),
            ("When people get hurt, they learn to hate… When people hurt others, they become hated and racked with guilt. But knowing that pain allows people to be kind. Pain allows people to grow… and how you grow is up to you.", "Jiraiya", 600),
            ("Searching for someone to blame is such a pain", "Gojo", 800),
            ("A person's life isn't so simple a matter, that it isn't. The true answer is something you find out yourself by how you live your life from this day forward", "Kenshin", 1000),
        ],
        "Pokemon": [
            ("This is the rarest pokeball - did Ash ever get one of these?", "master ball", 100),
            ("This pokemon has the ability to speak in human language - maybe we're all pokemon?", "meowth", 200),
            ("This is Ash Ketchum's hometown - where his mom, Mr. Mime and Professor Oak probably get freaky.", "pallet town", 300),
            ("Shiny pokemon are pokemon of a different color. This is the color of a shiny Charizard!", "black", 400),
            ("This pokemon has the ability to change its type depending on the item it's holding?", "arceus", 500),
        ],
        "Shoujo": [
            ("This shoujo anime is about a schoolgirl that transforms into a magical warrior and protects Earth from evil forces with the help of her classmates.", "sailor moon", 100),
            ("This shoujo/shonen anime is about a teenage martial artist that transforms into a girl when splashed with cold water", "ranma", 200),
            ("This shoujo anime is about a kind-hearted girl who becomes entangled with a cursed family whose members transform into animals of the chinese zodiac when hugged by the opposite sex", "fruits basket", 300),
            ("This shoujo anime is famous because it portrayed a scholarship student at a prestigious school who accidentally stumbles into the school's host club and is mistaken for a boy, leading her to work as a host to repay debt.", "ouran", 400),
            ("This shoujo anime is Iskander's favorite. It's about an ordinary girl who attends an elite school where she clashes with the F4, a group of wealthy and influential boys, and finds herself entangled in a complicated love triangle.", "boys over flowers", 500),
        ],
        "Naruto": [
            ("This was the first jutsu Naruto mastered; it was forbidden", "shadow clone", 100),
            ("In a fun turn of irony, this person gave Naruto his first kiss", "sasuke", 200),
            ("This organization hunted the tailed beasts throughout Shippuden", "akatsuki", 300),
            ("This hokage is known as 'The Professor' - this is probably because of his proficiency with chakra types", "third", 400),
            ("This jutsu proved to be extremely effective against Kaguya - proving that even the Otsutsuki clan possessed vulnerabilities", "sexy jutsu", 500),
        ]
    }
    return jeopardy_questions