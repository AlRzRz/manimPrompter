from manim import *

class Step1Scene(Scene):
    def construct(self):
        content = "The problem asks for the definite integral ∫ from x=2 to x=4 of (-x^2 + 5x + 6) dx; this uses the given polynomial over the interval [2,4]."
        text = Text(content)
        self.play(Write(text))
        self.wait(2)
        self.play(FadeOut(text))
        self.wait(0.5)

class Step2Scene(Scene):
    def construct(self):
        content = "Let f(x) = -x^2 + 5x + 6. The integral computes the net area under the curve y = f(x) between x = 2 and x = 4 (a definite integral; related to area/accumulation)."
        text = Text(content)
        self.play(Write(text))
        self.wait(2)
        self.play(FadeOut(text))
        self.wait(0.5)

class Step3Scene(Scene):
    def construct(self):
        formula = MathTex(r"F(x) = \int (-x^2 + 5x + 6)\,dx = -\frac{1}{3}x^3 + \frac{5}{2}x^2 + 6x + C")
        formula.move_to(ORIGIN)
        self.play(Write(formula))
        self.wait(2)
        self.play(FadeOut(formula))
        self.wait(0.5)

class Step4Scene(Scene):
    def construct(self):
        formula = MathTex(r"F(4) = -\frac{1}{3}(4)^3 + \frac{5}{2}(4)^2 + 6(4) = -\frac{64}{3} + 80 + 24 = \frac{248}{3}")
        formula.move_to(ORIGIN)
        self.play(Write(formula))
        self.wait(2)
        self.play(FadeOut(formula))
        self.wait(0.5)

class Step5Scene(Scene):
    def construct(self):
        formula = MathTex(r"F(2) = -\frac{1}{3}(2)^3 + \frac{5}{2}(2)^2 + 6(2) = -\frac{8}{3} + 10 + 12 = \frac{58}{3}")
        formula.move_to(ORIGIN)
        self.play(Write(formula))
        self.wait(2)
        self.play(FadeOut(formula))
        self.wait(0.5)

class Step6Scene(Scene):
    def construct(self):
        formula = MathTex(r"\displaystyle \int_{2}^{4} (-x^2 + 5x + 6)\,dx = F(4) - F(2) = \frac{248}{3} - \frac{58}{3} = \frac{190}{3}")
        formula.move_to(ORIGIN)
        self.play(Write(formula))
        self.wait(2)
        self.play(FadeOut(formula))
        self.wait(0.5)

class Step7Scene(Scene):
    def construct(self):
        content = ("The value is 190/3. It represents the net area between y = -x^2 + 5x + 6 and the x-axis from x = 2 to x = 4; since the function is positive on [2,4], this is the area under the curve on that interval.")
        text = Text(content)
        self.play(Write(text))
        self.wait(2)
        self.play(FadeOut(text))
        self.wait(0.5) 