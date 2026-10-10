import sympy as sp


class MathFormatter:
    """
    Converts SymPy mathematics into human-readable
    Unicode mathematics for KRISHNA's terminal output.
    """

    def format(self, expression):
        """
        Convert a SymPy expression into readable Unicode math.
        """

        try:
            if isinstance(expression, str):
                expression = sp.sympify(
                    expression.replace("^", "**")
                )

            expression = sp.simplify(expression)

            # SymPy's Unicode pretty printer
            return sp.pretty(
                expression,
                use_unicode=True
            )

        except Exception:
            return str(expression)

    def format_result(self, label, expression):
        """
        Format a complete KRISHNA answer.
        """

        formatted = self.format(expression)

        return (
            f"{label}\n"
            f"{formatted}"
        )

    def format_derivative(self, expression):
        """
        Format derivative result.
        """

        formatted = self.format(expression)

        return (
            "The derivative is:\n"
            f"dy/dx = {formatted}"
        )

    def format_integral(self, expression):
        """
        Format integral result.
        """

        formatted = self.format(expression)

        return (
            "The integral is:\n"
            f"∫ = {formatted}"
        )

    def format_solution(self, solution):
        """
        Format equation solutions.
        """

        if isinstance(solution, list):

            formatted_values = []

            for value in solution:
                formatted_values.append(
                    self.format(value)
                )

            return ", ".join(formatted_values)

        return self.format(solution)