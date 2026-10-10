import re
import sympy as sp

from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
)


class MathEngine:
    """
    KRISHNA Advanced Mathematics Engine.

    Uses SymPy for symbolic and numerical mathematics.

    Supports:
        - Arithmetic
        - Natural-language arithmetic
        - Algebra
        - Equations
        - Systems of equations
        - Derivatives
        - Partial derivatives
        - Integrals
        - Definite integrals
        - Limits
        - Factorization
        - Expansion
        - Simplification
        - Trigonometry
        - Logarithms
        - Roots
        - Numerical evaluation
        - Fractions
        - Percentages

    Mathematical results are converted into
    compact, human-readable Unicode notation.
    """

    def __init__(self):

        # =====================================================
        # COMMON SYMBOLS
        # =====================================================

        self.x = sp.Symbol("x")
        self.y = sp.Symbol("y")
        self.z = sp.Symbol("z")

        self.t = sp.Symbol("t")
        self.n = sp.Symbol("n")

        self.a = sp.Symbol("a")
        self.b = sp.Symbol("b")
        self.c = sp.Symbol("c")

        # =====================================================
        # PARSER TRANSFORMATIONS
        # =====================================================

        self.transformations = standard_transformations + (
            convert_xor,
            implicit_multiplication_application,
        )

        # =====================================================
        # SAFE MATHEMATICAL FUNCTIONS / CONSTANTS
        # =====================================================

        self.local_dict = {

            # Variables
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "t": self.t,
            "n": self.n,
            "a": self.a,
            "b": self.b,
            "c": self.c,

            # Constants
            "pi": sp.pi,
            "e": sp.E,
            "E": sp.E,
            "oo": sp.oo,
            "inf": sp.oo,
            "infinity": sp.oo,

            # Basic functions
            "sqrt": sp.sqrt,
            "abs": sp.Abs,
            "Abs": sp.Abs,

            # Trigonometry
            "sin": sp.sin,
            "cos": sp.cos,
            "tan": sp.tan,
            "cot": sp.cot,
            "sec": sp.sec,
            "csc": sp.csc,

            # Inverse trigonometry
            "asin": sp.asin,
            "acos": sp.acos,
            "atan": sp.atan,

            # Hyperbolic
            "sinh": sp.sinh,
            "cosh": sp.cosh,
            "tanh": sp.tanh,

            # Logarithms
            "log": sp.log,
            "ln": sp.log,

            # Exponential
            "exp": sp.exp,

            # Combinatorics
            "factorial": sp.factorial,
            "fact": sp.factorial,

            # Special functions
            "gamma": sp.gamma,
        }

    # =========================================================
    # MATHEMATICAL FORMATTER
    # =========================================================

    def format_math(self, expression):
        """
        Convert a SymPy expression into compact,
        human-readable mathematical notation.

        Examples:

            3*x**2
                ↓
            3x²

            x**3/3
                ↓
            x³/3

            sqrt(x)
                ↓
            √x

            pi*x
                ↓
            πx

            -3*x
                ↓
            −3x
        """

        try:

            expression = sp.simplify(expression)

            # Get normal SymPy string representation.
            text = str(expression)

            # -------------------------------------------------
            # Replace powers first
            # -------------------------------------------------

            superscripts = {
                "0": "⁰",
                "1": "¹",
                "2": "²",
                "3": "³",
                "4": "⁴",
                "5": "⁵",
                "6": "⁶",
                "7": "⁷",
                "8": "⁸",
                "9": "⁹",
                "+": "⁺",
                "-": "⁻",
                "(": "⁽",
                ")": "⁾",
            }

            def power_to_superscript(match):

                power = match.group(1)

                result = ""

                for char in power:

                    result += superscripts.get(
                        char,
                        char
                    )

                return result

            # x**2 → x²
            # x**10 → x¹⁰
            text = re.sub(
                r"\*\*([0-9+\-()]+)",
                power_to_superscript,
                text
            )

            # -------------------------------------------------
            # Mathematical symbols
            # -------------------------------------------------

            text = text.replace(
                "sqrt(",
                "√("
            )

            text = text.replace(
                "pi",
                "π"
            )

            text = text.replace(
                "oo",
                "∞"
            )

            # -------------------------------------------------
            # Multiplication
            # -------------------------------------------------

            # 3*x → 3x
            # x*y → xy
            # 2*(x + 1) → 2(x + 1)

            text = text.replace(
                "*",
                ""
            )

            # -------------------------------------------------
            # Negative sign
            # -------------------------------------------------

            text = text.replace(
                "-",
                "−"
            )

            # -------------------------------------------------
            # Remove unnecessary spaces
            # -------------------------------------------------

            text = re.sub(
                r"\s+",
                " ",
                text
            )

            # -------------------------------------------------
            # Clean simple square roots
            # -------------------------------------------------

            text = re.sub(
                r"√\(([^()]+)\)",
                r"√\1",
                text
            )

            return text.strip()

        except Exception:

            return str(expression)

    # =========================================================
    # INLINE FORMATTER
    # =========================================================

    def format_inline(self, expression):
        """
        Compact one-line mathematical formatting.

        Designed for expressions appearing inside
        equations such as:

            ∫ x² dx
            dy/dx = 3x²
        """

        return self.format_math(
            expression
        )

    # =========================================================
    # MAIN SOLVER
    # =========================================================

    def solve(self, user_input):

        if not user_input:

            return (
                "Please give me a mathematics problem."
            )

        text = user_input.strip().lower()

        try:

            # Normalize natural language.
            text = self.normalize_text(text)

            # -------------------------------------------------
            # LIMIT
            # -------------------------------------------------

            if self.contains_any(
                text,
                [
                    "limit",
                    "lim as",
                    "lim when",
                    "lim x tends",
                    "limit as",
                ]
            ):

                return self.solve_limit(
                    text
                )

            # -------------------------------------------------
            # DIFFERENTIATION
            # -------------------------------------------------

            if self.contains_any(
                text,
                [
                    "differentiate",
                    "derivative",
                    "d/dx",
                    "find dy dx",
                ]
            ):

                return self.solve_derivative(
                    text
                )

            # -------------------------------------------------
            # INTEGRATION
            # -------------------------------------------------

            if self.contains_any(
                text,
                [
                    "integrate",
                    "integration",
                    "integral",
                    "find integral",
                ]
            ):

                return self.solve_integral(
                    text
                )

            # -------------------------------------------------
            # FACTORIZATION
            # -------------------------------------------------

            if self.contains_any(
                text,
                [
                    "factorize",
                    "factorise",
                    "factor",
                ]
            ):

                expression = self.extract_expression(
                    text
                )

                result = sp.factor(
                    self.parse(expression)
                )

                return (
                    "The factored form is:\n"
                    f"{self.format_math(result)}"
                )

            # -------------------------------------------------
            # EXPANSION
            # -------------------------------------------------

            if self.contains_any(
                text,
                [
                    "expand",
                    "expansion",
                ]
            ):

                expression = self.extract_expression(
                    text
                )

                result = sp.expand(
                    self.parse(expression)
                )

                return (
                    "The expanded form is:\n"
                    f"{self.format_math(result)}"
                )

            # -------------------------------------------------
            # SIMPLIFICATION
            # -------------------------------------------------

            if self.contains_any(
                text,
                [
                    "simplify",
                    "simplification",
                ]
            ):

                expression = self.extract_expression(
                    text
                )

                result = sp.simplify(
                    self.parse(expression)
                )

                return (
                    "The simplified result is:\n"
                    f"{self.format_math(result)}"
                )

            # -------------------------------------------------
            # EQUATION
            # -------------------------------------------------

            if (
                "=" in text
                or self.contains_any(
                    text,
                    [
                        "solve",
                        "find x",
                        "find roots",
                        "roots of",
                    ]
                )
            ):

                return self.solve_equation(
                    text
                )

            # -------------------------------------------------
            # NUMERICAL CALCULATION
            # -------------------------------------------------

            if self.contains_any(
                text,
                [
                    "evaluate",
                    "calculate",
                    "compute",
                    "what is",
                    "find value",
                    "value of",
                ]
            ):

                return self.calculate(
                    text
                )

            # -------------------------------------------------
            # DEFAULT
            # -------------------------------------------------

            return self.calculate(
                text
            )

        except Exception as error:

            return (
                "I couldn't solve that mathematics problem.\n"
                "Please check the expression.\n"
                f"Details: {error}"
            )

    # =========================================================
    # NATURAL LANGUAGE NORMALIZATION
    # =========================================================

    def normalize_text(self, text):

        replacements = {

            # Arithmetic
            "multiplied by": "*",
            "multiply by": "*",
            "divided by": "/",
            "divide by": "/",
            "times": "*",
            "plus": "+",
            "add": "+",
            "minus": "-",
            "subtract": "-",
            "over": "/",

            # Powers
            "to the power of": "**",
            "raised to": "**",

            # Equality
            "equals": "=",
            "equal to": "=",

            # Roots
            "square root of": "sqrt(",
        }

        # Longer phrases first.
        for old, new in sorted(
            replacements.items(),
            key=lambda item: len(item[0]),
            reverse=True
        ):

            text = text.replace(
                old,
                new
            )

        # -----------------------------------------------------
        # Square root
        # -----------------------------------------------------

        if "sqrt(" in text:

            match = re.search(
                r"sqrt\(([^()]+)$",
                text
            )

            if match:

                text += ")"

        # -----------------------------------------------------
        # Percentage
        # -----------------------------------------------------

        text = re.sub(
            r"(\d+(?:\.\d+)?)\s*%",
            r"(\1/100)",
            text
        )

        # -----------------------------------------------------
        # Remove conversational phrases
        # -----------------------------------------------------

        phrases = [
            "please",
            "can you",
            "could you",
            "tell me",
            "calculate",
            "compute",
            "evaluate",
        ]

        for phrase in phrases:

            text = text.replace(
                phrase,
                ""
            )

        return text.strip()

    # =========================================================
    # SAFE EXPRESSION PARSER
    # =========================================================

    def parse(self, expression):

        expression = expression.strip()

        if not expression:

            raise ValueError(
                "No mathematical expression was provided."
            )

        if len(expression) > 500:

            raise ValueError(
                "Expression is too long."
            )

        # -----------------------------------------------------
        # Security checks
        # -----------------------------------------------------

        forbidden = [
            "__",
            "import",
            "exec",
            "eval",
            "lambda",
            "open(",
            "os.",
            "sys.",
            "subprocess",
        ]

        lowered = expression.lower()

        for item in forbidden:

            if item in lowered:

                raise ValueError(
                    "Unsupported expression."
                )

        # -----------------------------------------------------
        # Allowed mathematical characters
        # -----------------------------------------------------

        if not re.fullmatch(
            r"[0-9a-zA-Z_+\-*/^().,\s=<>\[\]]+",
            expression
        ):

            raise ValueError(
                "Expression contains unsupported characters."
            )

        return parse_expr(
            expression,
            local_dict=self.local_dict,
            transformations=self.transformations,
            evaluate=True
        )

    # =========================================================
    # EXTRACT EXPRESSION
    # =========================================================

    def extract_expression(self, text):

        text = text.strip()

        prefixes = [
            "what is",
            "calculate",
            "compute",
            "evaluate",
            "find",
            "please",
            "can you",
            "could you",
            "simplify",
            "factorize",
            "factorise",
            "factor",
            "expand",
            "expansion",
        ]

        for prefix in prefixes:

            text = text.replace(
                prefix,
                ""
            )

        return text.strip()

    # =========================================================
    # BASIC CALCULATION
    # =========================================================

    def calculate(self, text):

        expression = self.extract_expression(
            text
        )

        result = self.parse(
            expression
        )

        simplified = sp.simplify(
            result
        )

        # -----------------------------------------------------
        # Exact numerical answer
        # -----------------------------------------------------

        if simplified.is_number:

            # Integer
            if simplified.is_Integer:

                return (
                    "The answer is: "
                    f"{self.format_math(simplified)}"
                )

            # Other exact numerical values
            formatted = self.format_math(
                simplified
            )

            numeric = sp.N(
                simplified,
                12
            )

            return (
                "The answer is:\n"
                f"{formatted}\n"
                f"≈ {numeric}"
            )

        # -----------------------------------------------------
        # Symbolic result
        # -----------------------------------------------------

        return (
            "The result is:\n"
            f"{self.format_math(simplified)}"
        )

    # =========================================================
    # EQUATIONS
    # =========================================================

    def solve_equation(self, text):

        equation_text = text.strip()

        equation_text = equation_text.replace(
            "solve",
            ""
        )

        equation_text = equation_text.replace(
            "find x",
            ""
        )

        equation_text = equation_text.replace(
            "roots of",
            ""
        )

        equation_text = equation_text.strip()

        # =====================================================
        # SYSTEM OF EQUATIONS
        # =====================================================

        if ";" in equation_text:

            equations = equation_text.split(
                ";"
            )

            parsed_equations = []

            for equation in equations:

                if "=" not in equation:

                    continue

                left, right = equation.split(
                    "=",
                    1
                )

                left_expr = self.parse(
                    left
                )

                right_expr = self.parse(
                    right
                )

                parsed_equations.append(
                    sp.Eq(
                        left_expr,
                        right_expr
                    )
                )

            if not parsed_equations:

                raise ValueError(
                    "Could not understand the equations."
                )

            variables = set()

            for equation in parsed_equations:

                variables.update(
                    equation.free_symbols
                )

            result = sp.solve(
                parsed_equations,
                list(variables),
                dict=True
            )

            if not result:

                return (
                    "No solution was found."
                )

            output = [
                "The solution is:"
            ]

            for solution in result:

                for variable, value in solution.items():

                    output.append(
                        f"{self.format_math(variable)} = "
                        f"{self.format_math(value)}"
                    )

            return "\n".join(
                output
            )

        # =====================================================
        # SINGLE EQUATION
        # =====================================================

        if "=" in equation_text:

            left, right = equation_text.split(
                "=",
                1
            )

            left_expr = self.parse(
                left
            )

            right_expr = self.parse(
                right
            )

            equation = sp.Eq(
                left_expr,
                right_expr
            )

            variables = list(
                equation.free_symbols
            )

            if not variables:

                if equation:

                    return (
                        "The equation is true."
                    )

                return (
                    "The equation is false."
                )

            result = sp.solve(
                equation,
                variables
            )

            if not result:

                return (
                    "No solution was found."
                )

            # One variable / one solution
            if len(variables) == 1:

                variable = variables[0]

                output = [
                    "The solution is:"
                ]

                for value in result:

                    output.append(
                        f"{self.format_math(variable)} = "
                        f"{self.format_math(value)}"
                    )

                return "\n".join(
                    output
                )

            # Multiple variables
            output = [
                "The solutions are:"
            ]

            for value in result:

                output.append(
                    self.format_math(value)
                )

            return "\n".join(
                output
            )

        # =====================================================
        # POLYNOMIAL ROOTS
        # =====================================================

        expression = self.extract_expression(
            equation_text
        )

        expr = self.parse(
            expression
        )

        variables = list(
            expr.free_symbols
        )

        if variables:

            result = sp.solve(
                expr,
                variables[0]
            )

            if not result:

                return (
                    "No roots/solutions were found."
                )

            output = [
                "The roots/solutions are:"
            ]

            for value in result:

                output.append(
                    self.format_math(value)
                )

            return "\n".join(
                output
            )

        return (
            "The expression evaluates to:\n"
            f"{self.format_math(sp.simplify(expr))}"
        )

    # =========================================================
    # DIFFERENTIATION
    # =========================================================

    def solve_derivative(self, text):

        expression = text

        patterns = [
            "find the derivative of",
            "find derivative of",
            "derivative of",
            "differentiate",
            "derivative",
            "d/dx",
        ]

        for pattern in patterns:

            expression = expression.replace(
                pattern,
                ""
            )

        expression = expression.strip()

        # -----------------------------------------------------
        # Detect variable
        # -----------------------------------------------------

        variable = self.detect_variable(
            expression
        )

        # -----------------------------------------------------
        # "with respect to x"
        # -----------------------------------------------------

        match = re.search(
            r"with respect to ([a-zA-Z]+)",
            expression
        )

        if match:

            variable_name = match.group(1)

            variable = sp.Symbol(
                variable_name
            )

            expression = re.sub(
                r"with respect to [a-zA-Z]+",
                "",
                expression
            )

        # -----------------------------------------------------
        # Parse expression
        # -----------------------------------------------------

        expr = self.parse(
            expression
        )

        # -----------------------------------------------------
        # Calculate derivative
        # -----------------------------------------------------

        result = sp.diff(
            expr,
            variable
        )

        result = sp.simplify(
            result
        )

        formatted_result = self.format_math(
            result
        )

        return (
            "The derivative is:\n"
            f"dy/d{variable} = "
            f"{formatted_result}"
        )

    # =========================================================
    # INTEGRATION
    # =========================================================

    def solve_integral(self, text):

        expression = text

        patterns = [
            "find the integral of",
            "find integral of",
            "integration of",
            "integral of",
            "integrate",
            "integration",
            "integral",
        ]

        for pattern in patterns:

            expression = expression.replace(
                pattern,
                ""
            )

        expression = expression.strip()

        # =====================================================
        # DEFINITE INTEGRAL
        #
        # Example:
        #
        # integrate x^2 from 0 to 2
        # =====================================================

        match = re.search(
            r"(.+?)\s+from\s+(.+?)\s+to\s+(.+)$",
            expression
        )

        if match:

            expr_text = match.group(1)
            lower_text = match.group(2)
            upper_text = match.group(3)

            expr = self.parse(
                expr_text
            )

            lower = self.parse(
                lower_text
            )

            upper = self.parse(
                upper_text
            )

            variable = self.detect_variable(
                expr_text
            )

            result = sp.integrate(
                expr,
                (
                    variable,
                    lower,
                    upper
                )
            )

            result = sp.simplify(
                result
            )

            formatted_expression = self.format_inline(
                expr
            )

            formatted_result = self.format_math(
                result
            )

            approximate = sp.N(
                result,
                10
            )

            return (
                "The definite integral is:\n"
                f"∫ {formatted_expression} "
                f"d{variable} = "
                f"{formatted_result}\n"
                f"≈ {approximate}"
            )

        # =====================================================
        # INDEFINITE INTEGRAL
        # =====================================================

        variable = self.detect_variable(
            expression
        )

        expr = self.parse(
            expression
        )

        result = sp.integrate(
            expr,
            variable
        )

        result = sp.simplify(
            result
        )

        formatted_expression = self.format_inline(
            expr
        )

        formatted_result = self.format_math(
            result
        )

        return (
            "The integral is:\n"
            f"∫ {formatted_expression} "
            f"d{variable} = "
            f"{formatted_result} + C"
        )

    # =========================================================
    # LIMIT
    # =========================================================

    def solve_limit(self, text):

        expression = text

        expression = expression.replace(
            "find limit",
            ""
        )

        expression = expression.replace(
            "limit",
            ""
        )

        expression = expression.replace(
            "lim",
            ""
        )

        expression = expression.strip()

        # =====================================================
        # Example:
        #
        # x^2 as x approaches 2
        # =====================================================

        match = re.search(
            r"(.+?)\s+as\s+([a-zA-Z]+)\s+"
            r"(?:approaches|tends to|goes to)\s+(.+)$",
            expression
        )

        if match:

            expr_text = match.group(1)
            variable_name = match.group(2)
            point_text = match.group(3)

            variable = sp.Symbol(
                variable_name
            )

            expr = self.parse(
                expr_text
            )

            point = self.parse(
                point_text
            )

            result = sp.limit(
                expr,
                variable,
                point
            )

            result = sp.simplify(
                result
            )

            return (
                "The limit is:\n"
                f"{self.format_math(result)}"
            )

        # =====================================================
        # Example:
        #
        # x^2 x -> 2
        # =====================================================

        match = re.search(
            r"(.+?)\s+([a-zA-Z]+)\s*->\s*(.+)$",
            expression
        )

        if match:

            expr_text = match.group(1)
            variable_name = match.group(2)
            point_text = match.group(3)

            variable = sp.Symbol(
                variable_name
            )

            expr = self.parse(
                expr_text
            )

            point = self.parse(
                point_text
            )

            result = sp.limit(
                expr,
                variable,
                point
            )

            result = sp.simplify(
                result
            )

            return (
                "The limit is:\n"
                f"{self.format_math(result)}"
            )

        raise ValueError(
            "Please specify the limit point.\n"
            "Example: limit x^2 as x approaches 2"
        )

    # =========================================================
    # VARIABLE DETECTION
    # =========================================================

    def detect_variable(self, expression):

        # Prefer x
        if re.search(
            r"\bx\b",
            expression
        ):

            return self.x

        # Then y
        if re.search(
            r"\by\b",
            expression
        ):

            return self.y

        # Then z
        if re.search(
            r"\bz\b",
            expression
        ):

            return self.z

        # Then t
        if re.search(
            r"\bt\b",
            expression
        ):

            return self.t

        # Inspect parsed symbols
        try:

            expr = self.parse(
                expression
            )

            symbols = list(
                expr.free_symbols
            )

            if symbols:

                return symbols[0]

        except Exception:

            pass

        # Default variable
        return self.x

    # =========================================================
    # HELPER
    # =========================================================

    @staticmethod
    def contains_any(
        text,
        phrases
    ):

        return any(
            phrase in text
            for phrase in phrases
        )