import re


class FormulaEngine:
    """
    KRISHNA Formula Engine.

    Provides accurate, readable mathematical formulas
    without depending on the AI model to generate them.

    The engine returns None when the question is not a
    recognized formula request, allowing KRISHNA to send
    the question to Gemini/Ollama normally.
    """

    def __init__(self):

        self.formulas = [

            # =================================================
            # GEOMETRY
            # =================================================

            {
                "keywords": [
                    "area of a circle",
                    "circle area",
                    "area circle"
                ],
                "answer": (
                    "The area of a circle is:\n\n"
                    "A = πr²\n\n"
                    "Where:\n"
                    "• A = area of the circle\n"
                    "• r = radius of the circle\n"
                    "• π ≈ 3.14159"
                )
            },

            {
                "keywords": [
                    "circumference of a circle",
                    "circle circumference",
                    "circumference circle"
                ],
                "answer": (
                    "The circumference of a circle is:\n\n"
                    "C = 2πr\n\n"
                    "Where:\n"
                    "• C = circumference\n"
                    "• r = radius\n"
                    "• π ≈ 3.14159"
                )
            },

            {
                "keywords": [
                    "area of a triangle",
                    "triangle area"
                ],
                "answer": (
                    "The area of a triangle is:\n\n"
                    "A = ½bh\n\n"
                    "Where:\n"
                    "• A = area\n"
                    "• b = base\n"
                    "• h = height"
                )
            },

            {
                "keywords": [
                    "area of a rectangle",
                    "rectangle area"
                ],
                "answer": (
                    "The area of a rectangle is:\n\n"
                    "A = lw\n\n"
                    "Where:\n"
                    "• A = area\n"
                    "• l = length\n"
                    "• w = width"
                )
            },

            {
                "keywords": [
                    "area of a square",
                    "square area"
                ],
                "answer": (
                    "The area of a square is:\n\n"
                    "A = a²\n\n"
                    "Where:\n"
                    "• A = area\n"
                    "• a = side length"
                )
            },

            {
                "keywords": [
                    "perimeter of a rectangle",
                    "rectangle perimeter"
                ],
                "answer": (
                    "The perimeter of a rectangle is:\n\n"
                    "P = 2(l + w)\n\n"
                    "Where:\n"
                    "• P = perimeter\n"
                    "• l = length\n"
                    "• w = width"
                )
            },

            {
                "keywords": [
                    "volume of a cube",
                    "cube volume"
                ],
                "answer": (
                    "The volume of a cube is:\n\n"
                    "V = a³\n\n"
                    "Where:\n"
                    "• V = volume\n"
                    "• a = side length"
                )
            },

            {
                "keywords": [
                    "volume of a sphere",
                    "sphere volume"
                ],
                "answer": (
                    "The volume of a sphere is:\n\n"
                    "V = ⁴⁄₃πr³\n\n"
                    "Where:\n"
                    "• V = volume\n"
                    "• r = radius"
                )
            },

            {
                "keywords": [
                    "surface area of a sphere",
                    "sphere surface area"
                ],
                "answer": (
                    "The surface area of a sphere is:\n\n"
                    "A = 4πr²\n\n"
                    "Where:\n"
                    "• A = surface area\n"
                    "• r = radius"
                )
            },

            {
                "keywords": [
                    "volume of a cylinder",
                    "cylinder volume"
                ],
                "answer": (
                    "The volume of a cylinder is:\n\n"
                    "V = πr²h\n\n"
                    "Where:\n"
                    "• V = volume\n"
                    "• r = radius\n"
                    "• h = height"
                )
            },

            {
                "keywords": [
                    "volume of a cone",
                    "cone volume"
                ],
                "answer": (
                    "The volume of a cone is:\n\n"
                    "V = ⅓πr²h\n\n"
                    "Where:\n"
                    "• V = volume\n"
                    "• r = radius\n"
                    "• h = height"
                )
            },

            {
                "keywords": [
                    "volume of a pyramid",
                    "pyramid volume"
                ],
                "answer": (
                    "The volume of a pyramid is:\n\n"
                    "V = ⅓Bh\n\n"
                    "Where:\n"
                    "• V = volume\n"
                    "• B = area of the base\n"
                    "• h = perpendicular height"
                )
            },

            # =================================================
            # HERON'S FORMULA
            # =================================================

            {
                "keywords": [
                    "heron's formula",
                    "heron formula",
                    "herons formula"
                ],
                "answer": (
                    "Heron's formula calculates the area of a "
                    "triangle when all three side lengths are known.\n\n"
                    "First calculate the semiperimeter:\n\n"
                    "s = (a + b + c) / 2\n\n"
                    "Then calculate the area:\n\n"
                    "A = √[s(s − a)(s − b)(s − c)]\n\n"
                    "Where:\n"
                    "• A = area of the triangle\n"
                    "• a, b, c = side lengths\n"
                    "• s = semiperimeter"
                )
            },

            # =================================================
            # PYTHAGOREAN THEOREM
            # =================================================

            {
                "keywords": [
                    "pythagorean theorem",
                    "pythagoras theorem",
                    "pythagorean formula",
                    "pythagoras formula"
                ],
                "answer": (
                    "The Pythagorean theorem is:\n\n"
                    "a² + b² = c²\n\n"
                    "Where:\n"
                    "• a and b = the two legs of a right triangle\n"
                    "• c = the hypotenuse"
                )
            },

            # =================================================
            # QUADRATIC FORMULA
            # =================================================

            {
                "keywords": [
                    "quadratic formula",
                    "formula for quadratic equation",
                    "quadratic equation formula"
                ],
                "answer": (
                    "The quadratic formula is:\n\n"
                    "x = (−b ± √(b² − 4ac)) / 2a\n\n"
                    "For a quadratic equation:\n\n"
                    "ax² + bx + c = 0\n\n"
                    "Where:\n"
                    "• a = coefficient of x²\n"
                    "• b = coefficient of x\n"
                    "• c = constant term"
                )
            },

            # =================================================
            # DISTANCE / SLOPE
            # =================================================

            {
                "keywords": [
                    "distance formula",
                    "formula for distance"
                ],
                "answer": (
                    "The distance formula is:\n\n"
                    "d = √[(x₂ − x₁)² + (y₂ − y₁)²]\n\n"
                    "Where:\n"
                    "• d = distance between two points\n"
                    "• (x₁, y₁) and (x₂, y₂) = the two points"
                )
            },

            {
                "keywords": [
                    "slope formula",
                    "formula for slope"
                ],
                "answer": (
                    "The slope formula is:\n\n"
                    "m = (y₂ − y₁) / (x₂ − x₁)\n\n"
                    "Where:\n"
                    "• m = slope\n"
                    "• (x₁, y₁) and (x₂, y₂) = two points"
                )
            },

            # =================================================
            # ALGEBRA
            # =================================================

            {
                "keywords": [
                    "difference of squares formula",
                    "difference of squares"
                ],
                "answer": (
                    "The difference of squares formula is:\n\n"
                    "a² − b² = (a − b)(a + b)"
                )
            },

            {
                "keywords": [
                    "perfect square formula",
                    "square expansion formula"
                ],
                "answer": (
                    "The common perfect-square identities are:\n\n"
                    "(a + b)² = a² + 2ab + b²\n\n"
                    "(a − b)² = a² − 2ab + b²"
                )
            },

            # =================================================
            # TRIGONOMETRY
            # =================================================

            {
                "keywords": [
                    "sine rule",
                    "sine law"
                ],
                "answer": (
                    "The sine rule is:\n\n"
                    "a / sin A = b / sin B = c / sin C"
                )
            },

            {
                "keywords": [
                    "cosine rule",
                    "cosine law"
                ],
                "answer": (
                    "The cosine rule is:\n\n"
                    "c² = a² + b² − 2ab cos C"
                )
            },

            {
                "keywords": [
                    "trigonometric identity",
                    "basic trigonometric identity"
                ],
                "answer": (
                    "A fundamental trigonometric identity is:\n\n"
                    "sin²θ + cos²θ = 1"
                )
            },

            # =================================================
            # PERCENTAGE / FINANCE
            # =================================================

            {
                "keywords": [
                    "simple interest formula",
                    "formula for simple interest"
                ],
                "answer": (
                    "The simple interest formula is:\n\n"
                    "SI = PRT / 100\n\n"
                    "Where:\n"
                    "• P = principal\n"
                    "• R = annual interest rate (%)\n"
                    "• T = time"
                )
            },

            {
                "keywords": [
                    "compound interest formula",
                    "formula for compound interest"
                ],
                "answer": (
                    "The compound amount formula is:\n\n"
                    "A = P(1 + r/n)ⁿᵗ\n\n"
                    "Compound interest is:\n\n"
                    "CI = A − P\n\n"
                    "Where:\n"
                    "• P = principal\n"
                    "• r = annual interest rate as a decimal\n"
                    "• n = number of compounding periods per year\n"
                    "• t = time"
                )
            },

            # =================================================
            # PHYSICS
            # =================================================

            {
                "keywords": [
                    "speed formula",
                    "formula for speed"
                ],
                "answer": (
                    "The speed formula is:\n\n"
                    "v = d / t\n\n"
                    "Where:\n"
                    "• v = speed\n"
                    "• d = distance\n"
                    "• t = time"
                )
            },

            {
                "keywords": [
                    "velocity formula",
                    "formula for velocity"
                ],
                "answer": (
                    "Average velocity is:\n\n"
                    "v = Δx / Δt\n\n"
                    "Where:\n"
                    "• v = average velocity\n"
                    "• Δx = displacement\n"
                    "• Δt = change in time"
                )
            },

            {
                "keywords": [
                    "acceleration formula",
                    "formula for acceleration"
                ],
                "answer": (
                    "The acceleration formula is:\n\n"
                    "a = Δv / Δt\n\n"
                    "Where:\n"
                    "• a = acceleration\n"
                    "• Δv = change in velocity\n"
                    "• Δt = change in time"
                )
            },

            {
                "keywords": [
                    "force formula",
                    "newton's second law",
                    "newtons second law"
                ],
                "answer": (
                    "Newton's second law is:\n\n"
                    "F = ma\n\n"
                    "Where:\n"
                    "• F = force\n"
                    "• m = mass\n"
                    "• a = acceleration"
                )
            },

            {
                "keywords": [
                    "work formula",
                    "formula for work"
                ],
                "answer": (
                    "The work formula is:\n\n"
                    "W = Fd cos θ\n\n"
                    "Where:\n"
                    "• W = work\n"
                    "• F = force\n"
                    "• d = displacement\n"
                    "• θ = angle between force and displacement"
                )
            },

            {
                "keywords": [
                    "power formula",
                    "formula for power"
                ],
                "answer": (
                    "The power formula is:\n\n"
                    "P = W / t\n\n"
                    "Where:\n"
                    "• P = power\n"
                    "• W = work\n"
                    "• t = time"
                )
            },

            {
                "keywords": [
                    "kinetic energy formula",
                    "formula for kinetic energy"
                ],
                "answer": (
                    "The kinetic energy formula is:\n\n"
                    "KE = ½mv²\n\n"
                    "Where:\n"
                    "• KE = kinetic energy\n"
                    "• m = mass\n"
                    "• v = velocity"
                )
            },

            {
                "keywords": [
                    "potential energy formula",
                    "gravitational potential energy",
                    "potential energy formula"
                ],
                "answer": (
                    "The gravitational potential energy formula is:\n\n"
                    "PE = mgh\n\n"
                    "Where:\n"
                    "• PE = potential energy\n"
                    "• m = mass\n"
                    "• g = gravitational acceleration\n"
                    "• h = height"
                )
            },

            {
                "keywords": [
                    "momentum formula",
                    "formula for momentum"
                ],
                "answer": (
                    "The momentum formula is:\n\n"
                    "p = mv\n\n"
                    "Where:\n"
                    "• p = momentum\n"
                    "• m = mass\n"
                    "• v = velocity"
                )
            },

            {
                "keywords": [
                    "density formula",
                    "formula for density"
                ],
                "answer": (
                    "The density formula is:\n\n"
                    "ρ = m / V\n\n"
                    "Where:\n"
                    "• ρ = density\n"
                    "• m = mass\n"
                    "• V = volume"
                )
            },

            # =================================================
            # ELECTRICITY
            # =================================================

            {
                "keywords": [
                    "ohm's law",
                    "ohms law",
                    "ohm law"
                ],
                "answer": (
                    "Ohm's law is:\n\n"
                    "V = IR\n\n"
                    "Where:\n"
                    "• V = voltage\n"
                    "• I = current\n"
                    "• R = resistance"
                )
            },

            {
                "keywords": [
                    "electric power formula",
                    "electrical power formula"
                ],
                "answer": (
                    "The electrical power formula is:\n\n"
                    "P = VI\n\n"
                    "Other equivalent forms are:\n\n"
                    "P = I²R\n"
                    "P = V²/R"
                )
            },
        ]

    # =========================================================
    # SOLVE FORMULA QUESTION
    # =========================================================

    def solve(self, user_input):

        if not user_input:
            return None

        text = self.normalize(
            user_input
        )

        # A formula request should normally contain
        # words such as formula, theorem, law, or "how".
        formula_request = (
            "formula" in text
            or "theorem" in text
            or "law" in text
            or "equation" in text
        )

        if not formula_request:
            return None

        # Search for known formulas.
        for item in self.formulas:

            for keyword in item["keywords"]:

                if keyword in text:

                    return (
                        "KRISHNA: "
                        + item["answer"]
                    )

        # No known formula.
        return None

    # =========================================================
    # NORMALIZATION
    # =========================================================

    def normalize(self, text):

        text = text.lower().strip()

        # Apostrophe variations
        text = text.replace(
            "’",
            "'"
        )

        # Remove unnecessary punctuation.
        text = re.sub(
            r"[?!.,]+$",
            "",
            text
        )

        # Normalize whitespace.
        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text