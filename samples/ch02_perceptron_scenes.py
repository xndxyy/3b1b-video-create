# 第二章（感知机）Manim 动画示例。
# 使用项目视觉规范中的颜色定义。

# -*- coding: utf-8 -*-
"""感知机视频 v2 — 3Blue1Brown风格Manim动画（详细版）"""
from manim import *
import numpy as np

# ============ 3Blue1Brown 官方配色 ============
BG = "#111111"
BLUE = "#58C4DD"
GOLD = "#F0AC5F"
PINK = "#D147BD"
GREEN = "#83C167"
PURPLE = "#9A72AC"
TEAL = "#5CD0B3"
ORANGE = "#FF862F"
RED_C = "#FC6255"
YELLOW = "#FFFF00"
WHITE = "#DDDDDD"
GREY_A = "#DDDDDD"
GREY_B = "#BBBBBB"
GREY_C = "#888888"
GREY_D = "#444444"
GREY_E = "#222222"
GREY_F = "#171717"

config.background_color = BG
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 30

# ============ 工具函数 ============
def make_label(text, color=WHITE, size=24, font="Consolas", weight=NORMAL):
    return Text(text, font_size=size, color=color, font=font, weight=weight)

def make_zh(text, color=WHITE, size=24, weight=NORMAL):
    return Text(text, font_size=size, color=color, font="Microsoft YaHei", weight=weight)

def make_panel(width, height, fill=GREY_E, fill_opacity=0.5, stroke=GREY_D, stroke_width=1):
    return Rectangle(width=width, height=height, fill_color=fill, fill_opacity=fill_opacity,
                     stroke_color=stroke, stroke_width=stroke_width)


# =====================================================================
# S1: 开场钩子
# =====================================================================
class S1_ColdOpen(Scene):
    def construct(self):
        # 扫描线
        scan = Line(LEFT * 7, RIGHT * 7, color=BLUE, stroke_width=2)
        scan.set_opacity(0.8)
        self.play(Create(scan), run_time=1.2, rate_func=linear)

        # 年份
        year = Text("1957", font_size=160, color=GOLD, font="Consolas", weight=BOLD)
        year.shift(UP * 0.5)
        self.play(Write(year), run_time=1.5)
        self.wait(0.5)

        # 副标题
        sub1 = make_zh("Frank Rosenblatt", size=22, color=GREY_B)
        sub1.next_to(year, DOWN, buff=0.6)
        sub2 = make_zh("康奈尔航空实验室", size=18, color=GREY_C)
        sub2.next_to(sub1, DOWN, buff=0.2)
        self.play(FadeIn(sub1, shift=UP*0.2), FadeIn(sub2), run_time=1.0)
        self.wait(2.5)

        # 切到标题
        title1 = make_zh("感知机", size=72, color=WHITE, weight=BOLD)
        title1.move_to(UP * 0.3)
        title2 = Text("Perceptron", font_size=36, color=GOLD, font="Consolas")
        title2.next_to(title1, DOWN, buff=0.4)
        self.play(
            FadeOut(year, shift=UP*0.5),
            FadeOut(sub1), FadeOut(sub2),
            FadeIn(title1, shift=UP*0.3),
            run_time=1.0
        )
        self.play(FadeIn(title2, shift=UP*0.2), run_time=0.8)
        self.wait(3)

        # 副标语
        tag = make_zh("深度学习最底层的那个公式", size=22, color=GREY_B)
        tag.to_edge(DOWN, buff=1.0)
        self.play(FadeIn(tag), run_time=0.8)
        self.wait(1.5)
        self.wait(13.9)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


# =====================================================================
# S2: 生物神经元
# =====================================================================
class S2_Bio(Scene):
    def construct(self):
        # 标题
        title = make_zh("从一颗生物神经元开始", size=36, color=WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.8)
        self.wait(0.5)
        self.play(title.animate.scale(0.7).to_edge(UP, buff=0.3), run_time=0.4)

        # 左侧：生物神经元
        # 细胞体
        soma = Ellipse(width=2.0, height=1.4, color=GREEN, fill_opacity=0.2, stroke_width=2)
        soma.move_to(LEFT * 3.5)

        # 树突（左边多分叉）
        dendrites = VGroup()
        for angle in [130, 145, 160, 175, 195, 210, 225]:
            d = Line(
                soma.get_left(),
                soma.get_left() + np.array([np.cos(angle * DEGREES), np.sin(angle * DEGREES), 0]) * 1.4,
                color=BLUE, stroke_width=2
            )
            # 加分叉
            tip = d.get_end()
            for sub_a in [-15, 0, 15]:
                branch = Line(
                    tip, tip + np.array([np.cos((angle + sub_a) * DEGREES),
                                        np.sin((angle + sub_a) * DEGREES), 0]) * 0.5,
                    color=BLUE, stroke_width=1.5
                )
                dendrites.add(branch)
            dendrites.add(d)

        # 轴突（右边一条长线）
        axon = Line(soma.get_right(), soma.get_right() + RIGHT * 2.5, color=TEAL, stroke_width=3)
        # 轴突末端的突触
        synapes = VGroup()
        for i, dy in enumerate([0.3, 0, -0.3]):
            s_tip = axon.get_end() + RIGHT * 0.0 + UP * dy
            for j, dx in enumerate([0.5, 1.0]):
                sp = Dot(s_tip + RIGHT * dx, radius=0.08, color=YELLOW)
                synapes.add(sp)

        bio_label = make_zh("生物神经元", size=20, color=GREY_B)
        bio_label.next_to(soma, DOWN, buff=2.3)
        self.play(
            GrowFromCenter(soma),
            Create(dendrites),
            Create(axon),
            run_time=1.5
        )
        self.play(FadeIn(synapes, lag_ratio=0.1), run_time=0.6)
        self.play(FadeIn(bio_label), run_time=0.4)
        self.wait(0.5)

        # 标注
        dend_label = make_zh("树突：接收", size=18, color=BLUE)
        dend_label.next_to(soma, LEFT, buff=1.2).shift(UP * 0.8)
        axon_label = make_zh("轴突：传出", size=18, color=TEAL)
        axon_label.next_to(axon, RIGHT, buff=0.3).shift(UP * 0.5)
        syn_label = make_zh("突触", size=18, color=YELLOW)
        syn_label.next_to(synapes, RIGHT, buff=0.3).shift(DOWN * 0.5)
        self.play(
            FadeIn(dend_label, shift=RIGHT*0.2),
            FadeIn(axon_label, shift=LEFT*0.2),
            FadeIn(syn_label, shift=LEFT*0.2),
            run_time=0.8
        )
        self.wait(1.0)

        # 信号动画：脉冲
        pulse = Dot(color=YELLOW, radius=0.12).move_to(axon.get_start())
        self.play(MoveAlongPath(pulse, axon), run_time=0.8, rate_func=linear)
        self.play(FadeOut(pulse), run_time=0.2)

        # 关键提示
        key = make_zh("要么不发射 · 要么全功率发射", size=22, color=GOLD, weight=BOLD)
        key.to_edge(DOWN, buff=0.6)
        self.play(FadeIn(key, shift=UP*0.3), run_time=0.6)
        self.wait(1.5)
        self.wait(15.8)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


# =====================================================================
# S3: 感知机结构
# =====================================================================
class S3_Structure(Scene):
    def construct(self):
        title = make_zh("感知机的结构", size=36, color=WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.6)

        # 输入节点
        in_pos = LEFT * 5.5
        x1 = Circle(radius=0.4, color=BLUE, fill_opacity=0.2, stroke_width=2).move_to(in_pos + UP * 1.8)
        x2 = Circle(radius=0.4, color=GREEN, fill_opacity=0.2, stroke_width=2).move_to(in_pos + DOWN * 1.8)
        x1t = Text("x₁", font_size=28, color=BLUE, font="Microsoft YaHei", weight=BOLD).move_to(x1)
        x2t = Text("x₂", font_size=28, color=GREEN, font="Microsoft YaHei", weight=BOLD).move_to(x2)

        in_label = make_zh("输入", size=18, color=GREY_C)
        in_label.next_to(x1, LEFT, buff=0.4)

        # 神经元
        neuron = Circle(radius=0.7, color=GOLD, fill_opacity=0.15, stroke_width=3).move_to(LEFT * 0.5)
        sigma = Text("Σ", font_size=44, color=GOLD, font="Microsoft YaHei", weight=BOLD).move_to(neuron)

        # 连线
        l1 = Line(x1.get_right(), neuron.get_left() + UP*0.3, color=GREY_C, stroke_width=2)
        l2 = Line(x2.get_right(), neuron.get_left() + DOWN*0.3, color=GREY_C, stroke_width=2)

        # 权重标签
        w1 = Text("w₁", font_size=24, color=YELLOW, font="Microsoft YaHei", weight=BOLD)
        w1.move_to(l1.get_center() + UP*0.4)
        w2 = Text("w₂", font_size=24, color=YELLOW, font="Microsoft YaHei", weight=BOLD)
        w2.move_to(l2.get_center() + DOWN*0.4)

        # 比较器
        cmp_box = RoundedRectangle(width=2.0, height=1.0, corner_radius=0.1,
                                   fill_color=GREY_E, fill_opacity=0.7,
                                   stroke_color=GREY_C, stroke_width=1.5)
        cmp_box.move_to(RIGHT * 2.0)
        cmp_txt = Text("> θ ?", font_size=28, color=WHITE, font="Microsoft YaHei", weight=BOLD).move_to(cmp_box)
        arrow_in = Arrow(neuron.get_right(), cmp_box.get_left(), buff=0.15, color=GREY_C, stroke_width=2)

        # 输出
        out_y = Circle(radius=0.4, color=GREEN, fill_opacity=0.3, stroke_width=2).move_to(RIGHT * 4.7 + UP * 1.0)
        out_n = Circle(radius=0.4, color=RED_C, fill_opacity=0.3, stroke_width=2).move_to(RIGHT * 4.7 + DOWN * 1.0)
        out_yt = Text("1", font_size=28, color=GREEN, font="Consolas", weight=BOLD).move_to(out_y)
        out_nt = Text("0", font_size=28, color=RED_C, font="Consolas", weight=BOLD).move_to(out_n)
        a_y = Arrow(cmp_box.get_right() + UP*0.15, out_y.get_left(), buff=0.15, color=GREEN, stroke_width=2)
        a_n = Arrow(cmp_box.get_right() + DOWN*0.15, out_n.get_left(), buff=0.15, color=RED_C, stroke_width=2)

        # 公式
        formula = Text("w₁·x₁ + w₂·x₂  >  θ     ⟹     y = 1",
                       font_size=30, color=GREY_B, font="Microsoft YaHei")
        formula.to_edge(DOWN, buff=1.0)

        # 构建动画
        self.play(GrowFromCenter(x1), GrowFromCenter(x2), run_time=0.6)
        self.play(FadeIn(x1t), FadeIn(x2t), FadeIn(in_label), run_time=0.4)
        self.play(Create(l1), Create(l2), run_time=0.6)
        self.play(FadeIn(w1, shift=UP*0.2), FadeIn(w2, shift=DOWN*0.2), run_time=0.4)
        self.play(GrowFromCenter(neuron), Write(sigma), run_time=0.6)
        self.play(GrowArrow(arrow_in), FadeIn(cmp_box), FadeIn(cmp_txt), run_time=0.5)
        self.play(GrowArrow(a_y), GrowArrow(a_n), run_time=0.4)
        self.play(FadeIn(out_y), FadeIn(out_n), FadeIn(out_yt), FadeIn(out_nt), run_time=0.4)
        self.play(Write(formula), run_time=1.0)
        self.wait(0.8)

        # 信号流脉冲
        for trial in range(2):
            d1 = Dot(color=BLUE, radius=0.1).move_to(x1)
            d2 = Dot(color=GREEN, radius=0.1).move_to(x2)
            self.play(MoveAlongPath(d1, l1), MoveAlongPath(d2, l2), run_time=0.5)
            self.play(neuron.animate.set_fill(GOLD, opacity=0.6), run_time=0.15)
            self.play(neuron.animate.set_fill(GOLD, opacity=0.15), run_time=0.15)
            self.play(out_y.animate.set_fill(GREEN, opacity=0.8), run_time=0.15)
            self.play(out_y.animate.set_fill(GREEN, opacity=0.3), run_time=0.15)
            self.remove(d1, d2)

        self.wait(0.5)

        # 强调权重的作用
        weight_note = make_zh("权重 = 信号线有多粗", size=24, color=YELLOW, weight=BOLD)
        weight_note.to_edge(DOWN, buff=0.3)
        self.play(FadeOut(formula), FadeIn(weight_note, shift=UP*0.3), run_time=0.6)
        self.wait(1.5)
        self.wait(15.8)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


# =====================================================================
# S4: 偏置项
# =====================================================================
class S4_Bias(Scene):
    def construct(self):
        title = make_zh("偏置：让决策边界可以平移", size=32, color=WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.6)
        self.wait(0.3)

        # 旧公式 (左上角)
        old = Text("w₁x₁ + w₂x₂  >  θ", font_size=36, color=GREY_B, font="Microsoft YaHei")
        old.to_corner(UL, buff=0.8).shift(DOWN * 0.6)
        self.play(Write(old), run_time=0.8)
        self.wait(0.3)

        # 箭头 + 注解
        transform_note = make_zh("把 θ 挪到等号左边 · 取反 · 改名", size=18, color=GREY_C)
        transform_note.next_to(old, DOWN, buff=0.3)
        self.play(FadeIn(transform_note), run_time=0.4)
        self.wait(0.3)

        # 新公式 (左上角)
        new = Text("w₁x₁ + w₂x₂  +  b  >  0", font_size=40, color=GOLD, font="Microsoft YaHei", weight=BOLD)
        new.to_corner(UL, buff=0.8).shift(DOWN * 0.6)
        self.play(
            FadeOut(transform_note),
            Transform(old, new),
            run_time=1.2
        )
        self.wait(0.5)

        # 解释 (左上角下方)
        b_label = make_zh("b = 偏置 bias", size=22, color=BLUE)
        b_label.next_to(old, DOWN, buff=0.5)
        b_note = make_zh("给决策边界一个平移的自由度", size=20, color=GREY_B)
        b_note.next_to(b_label, DOWN, buff=0.3)
        self.play(FadeIn(b_label, shift=UP*0.2), run_time=0.5)
        self.play(FadeIn(b_note, shift=UP*0.2), run_time=0.5)
        self.wait(1.0)

        # 几何演示：坐标系 + 直线平移 (右下角)
        axes = Axes(
            x_range=[-1, 4, 1], y_range=[-1, 4, 1],
            x_length=4.5, y_length=4.5,
            axis_config={"color": GREY_D, "stroke_width": 1.5},
        ).shift(RIGHT * 3.5 + DOWN * 0.5)

        x_lbl = Text("x₁", font_size=20, color=WHITE, font="Microsoft YaHei").next_to(axes.x_axis, RIGHT, buff=0.15)
        y_lbl = Text("x₂", font_size=20, color=WHITE, font="Microsoft YaHei").next_to(axes.y_axis, UP, buff=0.15)

        # 直线1：b=0
        line1 = axes.plot(lambda x: -x + 2, x_range=[-0.5, 3.5], color=RED_C, stroke_width=3)
        lbl1 = Text("b = 0", font_size=18, color=RED_C, font="Consolas").next_to(line1, UR, buff=0.1)

        # 直线2：b>0, 平移
        line2 = axes.plot(lambda x: -x + 3.5, x_range=[-0.5, 3.5], color=GREEN, stroke_width=3)
        lbl2 = Text("b > 0", font_size=18, color=GREEN, font="Consolas").next_to(line2, UR, buff=0.1)

        # 直线3：b<0
        line3 = axes.plot(lambda x: -x + 0.5, x_range=[-0.5, 3.5], color=BLUE, stroke_width=3)
        lbl3 = Text("b < 0", font_size=18, color=BLUE, font="Consolas").next_to(line3, UR, buff=0.1)

        # 数据点
        dots = VGroup(*[Dot(axes.c2p(x, y), radius=0.08, color=GREY_C) for x, y in [(1,1), (2,2), (3,3)]])

        self.play(Create(axes), FadeIn(x_lbl), FadeIn(y_lbl), run_time=0.8)
        self.play(FadeIn(dots), run_time=0.4)
        self.play(Create(line1), FadeIn(lbl1), run_time=0.7)
        self.wait(0.5)
        self.play(Transform(line1, line2), Transform(lbl1, lbl2), run_time=0.8)
        self.wait(0.3)
        self.play(Transform(line1, line3), Transform(lbl1, lbl3), run_time=0.8)
        self.wait(0.5)

        # 强调文字 (底部居中)
        em = make_zh("不经过原点", size=24, color=GOLD, weight=BOLD)
        em.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(em, shift=UP*0.3), run_time=0.6)
        self.wait(17.2)  # 等待voice继续
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


# =====================================================================
# S5: 简单逻辑门
# =====================================================================
class S5_LogicGates(Scene):
    def construct(self):
        # 标题
        title = make_zh("同一个结构 · 三个身份", size=36, color=WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.6)
        self.wait(0.3)
        self.play(title.animate.scale(0.7).to_edge(UP, buff=0.2), run_time=0.4)

        # ========== AND 门 ==========
        and_name = make_zh("AND 与门", size=32, color=GOLD, weight=BOLD)
        and_name.move_to(LEFT * 4 + UP * 1.0)
        and_params = Text("w = (0.5, 0.5)   b = -0.7", font_size=22, color=ORANGE, font="Consolas")
        and_params.next_to(and_name, DOWN, buff=0.2)

        # AND真值表
        and_table = VGroup()
        header_and = Text("x₁  x₂  →  y", font_size=22, color=WHITE, font="Microsoft YaHei", weight=BOLD)
        header_and.move_to(LEFT * 4 + DOWN * 0.2)
        and_table.add(header_and)
        and_rows = []
        for i, (a, b, y, hl) in enumerate([("0","0","0",False),("0","1","0",False),("1","0","0",False),("1","1","1",True)]):
            c = GOLD if hl else GREY_B
            row = Text(f" {a}    {b}    →    {y}", font_size=22, color=c, font="Consolas")
            row.move_to(LEFT * 4 + DOWN * (0.7 + i*0.45))
            and_table.add(row)
            and_rows.append((row, hl))

        self.play(FadeIn(and_name, shift=RIGHT*0.3), FadeIn(and_params), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(m) for m in and_table], lag_ratio=0.1), run_time=1.0)
        self.wait(0.5)
        # 高亮(1,1)行
        hl_box = SurroundingRectangle(and_rows[3][0], color=GOLD, buff=0.1, stroke_width=2)
        self.play(Create(hl_box), run_time=0.4)
        self.wait(1.2)

        # ========== NAND 门 ==========
        nand_name = make_zh("NAND 与非门", size=32, color=PINK, weight=BOLD)
        nand_name.move_to(LEFT * 4 + UP * 1.0)
        nand_params = Text("w = (-0.5, -0.5)   b = 0.7", font_size=22, color=ORANGE, font="Consolas")
        nand_params.next_to(nand_name, DOWN, buff=0.2)

        nand_table = VGroup()
        header_nand = Text("x₁  x₂  →  y", font_size=22, color=WHITE, font="Microsoft YaHei", weight=BOLD)
        header_nand.move_to(LEFT * 4 + DOWN * 0.2)
        nand_table.add(header_nand)
        nand_rows = []
        for i, (a, b, y, hl) in enumerate([("0","0","1",True),("0","1","1",True),("1","0","1",True),("1","1","0",False)]):
            c = PINK if hl else GREY_B
            row = Text(f" {a}    {b}    →    {y}", font_size=22, color=c, font="Consolas")
            row.move_to(LEFT * 4 + DOWN * (0.7 + i*0.45))
            nand_table.add(row)
            nand_rows.append((row, hl))

        self.play(
            Transform(and_name, nand_name),
            Transform(and_params, nand_params),
            FadeOut(hl_box),
            run_time=0.6
        )
        self.play(LaggedStart(*[FadeIn(m) for m in nand_table], lag_ratio=0.08), run_time=0.9)
        self.wait(0.5)
        # 高亮前三行
        hl_nand = VGroup(*[SurroundingRectangle(r[0], color=PINK, buff=0.1, stroke_width=2) for r in nand_rows[:3]])
        self.play(Create(hl_nand), run_time=0.5)
        self.wait(1.2)

        # ========== OR 门 ==========
        or_name = make_zh("OR 或门", size=32, color=BLUE, weight=BOLD)
        or_name.move_to(LEFT * 4 + UP * 1.0)
        or_params = Text("w = (0.5, 0.5)   b = -0.2", font_size=22, color=ORANGE, font="Consolas")
        or_params.next_to(or_name, DOWN, buff=0.2)

        or_table = VGroup()
        header_or = Text("x₁  x₂  →  y", font_size=22, color=WHITE, font="Microsoft YaHei", weight=BOLD)
        header_or.move_to(LEFT * 4 + DOWN * 0.2)
        or_table.add(header_or)
        or_rows = []
        for i, (a, b, y, hl) in enumerate([("0","0","0",False),("0","1","1",True),("1","0","1",True),("1","1","1",True)]):
            c = BLUE if hl else GREY_B
            row = Text(f" {a}    {b}    →    {y}", font_size=22, color=c, font="Consolas")
            row.move_to(LEFT * 4 + DOWN * (0.7 + i*0.45))
            or_table.add(row)
            or_rows.append((row, hl))

        self.play(
            Transform(and_name, or_name),
            Transform(and_params, or_params),
            FadeOut(hl_nand),
            run_time=0.6
        )
        self.play(LaggedStart(*[FadeIn(m) for m in or_table], lag_ratio=0.08), run_time=0.9)
        self.wait(0.5)
        hl_or = VGroup(*[SurroundingRectangle(r[0], color=BLUE, buff=0.1, stroke_width=2) for r in or_rows[1:]])
        self.play(Create(hl_or), run_time=0.5)
        self.wait(1.5)

        # 总结
        summary = make_zh("权重和偏置 = 三张面具", size=30, color=GOLD, weight=BOLD)
        summary.to_edge(DOWN, buff=0.6)
        self.play(FadeOut(hl_or), FadeIn(summary, shift=UP*0.3), run_time=0.8)
        self.wait(1.5)
        self.wait(18.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


# =====================================================================
# S6: 几何视角
# =====================================================================
class S6_Geometric(Scene):
    def construct(self):
        title = make_zh("几何视角：感知机 = 一条直线", size=32, color=WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.6)
        self.wait(0.3)
        self.play(title.animate.scale(0.65).to_edge(UP, buff=0.2), run_time=0.4)

        # 坐标系
        axes = Axes(
            x_range=[-0.3, 1.6, 1], y_range=[-0.3, 1.6, 1],
            x_length=5.5, y_length=5.5,
            axis_config={"color": GREY_D, "stroke_width": 1.5},
        ).shift(LEFT * 0.5)
        x_lbl = Text("x₁", font_size=22, color=WHITE, font="Microsoft YaHei").next_to(axes.x_axis, RIGHT, buff=0.15)
        y_lbl = Text("x₂", font_size=22, color=WHITE, font="Microsoft YaHei").next_to(axes.y_axis, UP, buff=0.15)
        self.play(Create(axes), FadeIn(x_lbl), FadeIn(y_lbl), run_time=0.8)

        # 四个点
        pts = [(0,0,RED_C,"○"), (0,1,GREEN,"△"), (1,0,GREEN,"△"), (1,1,RED_C,"○")]
        dots = VGroup()
        labels = VGroup()
        for x, y, col, sym in pts:
            d = Dot(axes.c2p(x, y), radius=0.13, color=col, fill_opacity=0.9)
            l = Text(sym, font_size=22, color=col, font="Microsoft YaHei", weight=BOLD)
            l.next_to(d, UR, buff=0.12)
            dots.add(d)
            labels.add(l)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.1), run_time=0.8)
        self.play(FadeIn(labels), run_time=0.4)
        self.wait(0.3)

        # 标签
        zero_lbl = make_zh("○ → y=0", size=18, color=RED_C)
        zero_lbl.move_to(RIGHT * 4.5 + UP * 2.0)
        one_lbl = make_zh("△ → y=1", size=18, color=GREEN)
        one_lbl.next_to(zero_lbl, DOWN, buff=0.3)
        self.play(FadeIn(zero_lbl), FadeIn(one_lbl), run_time=0.5)
        self.wait(0.3)

        # 第一条直线
        line = axes.plot(lambda x: -x + 1.3, x_range=[-0.2, 1.5], color=GOLD, stroke_width=3)
        line_lbl = Text("w₁x₁ + w₂x₂ + b = 0", font_size=18, color=GOLD, font="Microsoft YaHei")
        line_lbl.next_to(axes, RIGHT, buff=0.0).shift(UP * 2.5)
        self.play(Create(line), FadeIn(line_lbl), run_time=1.0)
        self.wait(0.5)

        # 平移演示
        for offset, color in [(0.5, ORANGE), (-0.3, TEAL), (1.0, PINK)]:
            new_line = axes.plot(lambda x, off=offset: -x + 1.3 + off,
                                x_range=[-0.2, 1.5], color=color, stroke_width=3)
            self.play(Transform(line, new_line), run_time=0.5)
            self.wait(0.3)

        # 强调：线性分类器
        em = make_zh("感知机 = 线性分类器", size=26, color=GOLD, weight=BOLD)
        em.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(em, shift=UP*0.3), run_time=0.6)
        self.wait(1.5)
        self.wait(17.8)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


# =====================================================================
# S7: XOR 困境
# =====================================================================
class S7_XOR(Scene):
    def construct(self):
        # 标题
        title = make_zh("期末考试：XOR 异或门", size=32, color=PINK, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.6)
        self.wait(0.3)
        self.play(title.animate.scale(0.7).to_edge(UP, buff=0.2), run_time=0.4)

        # 坐标系
        axes = Axes(
            x_range=[-0.3, 1.6, 1], y_range=[-0.3, 1.6, 1],
            x_length=5.5, y_length=5.5,
            axis_config={"color": GREY_D, "stroke_width": 1.5},
        ).shift(LEFT * 0.5)
        x_lbl = Text("x₁", font_size=22, color=WHITE, font="Microsoft YaHei").next_to(axes.x_axis, RIGHT, buff=0.15)
        y_lbl = Text("x₂", font_size=22, color=WHITE, font="Microsoft YaHei").next_to(axes.y_axis, UP, buff=0.15)
        self.play(Create(axes), FadeIn(x_lbl), FadeIn(y_lbl), run_time=0.6)

        # XOR点：(0,0)和(1,1)是○；其他是△
        pts = [(0,0,RED_C,"○"), (0,1,GREEN,"△"), (1,0,GREEN,"△"), (1,1,RED_C,"○")]
        dots = VGroup()
        labels = VGroup()
        for x, y, col, sym in pts:
            d = Dot(axes.c2p(x, y), radius=0.14, color=col, fill_opacity=0.9)
            l = Text(sym, font_size=22, color=col, font="Microsoft YaHei", weight=BOLD)
            l.next_to(d, UR, buff=0.12)
            dots.add(d)
            labels.add(l)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.12), run_time=0.8)
        self.play(FadeIn(labels), run_time=0.4)
        self.wait(0.3)

        # 强调X形
        xmark = make_zh("X 形分布", size=24, color=GOLD, weight=BOLD)
        xmark.to_edge(RIGHT, buff=1.0).shift(UP * 2)
        self.play(FadeIn(xmark), run_time=0.4)
        self.wait(0.5)

        # 尝试各种直线
        attempts = [
            lambda x: -x + 0.5,    # 1
            lambda x: 0.5,         # 2 水平
            lambda x: x + 0.5,     # 3
            lambda x: -0.5*x + 0.5 # 4
        ]
        for i, f in enumerate(attempts):
            line = axes.plot(f, x_range=[-0.2, 1.5], color=GOLD, stroke_width=3)
            self.play(Create(line), run_time=0.4)
            self.wait(0.3)
            # 加失败标记
            fail = Text("✗", font_size=28, color=RED_C, font="Microsoft YaHei", weight=BOLD)
            fail.move_to(axes.c2p(0.5, 1.3))
            self.play(FadeIn(fail, scale=1.5), run_time=0.2)
            self.wait(0.2)
            self.play(FadeOut(fail), FadeOut(line), run_time=0.3)

        # 大红叉
        big_x = Text("✗", font_size=140, color=RED_C, font="Microsoft YaHei", weight=BOLD)
        big_x.move_to(axes)
        self.play(FadeIn(big_x, scale=2), run_time=0.5)
        self.wait(0.8)

        # 结论
        conclusion = make_zh("单层感知机 = 一条直线 = 做不到", size=24, color=RED_C, weight=BOLD)
        conclusion.to_edge(DOWN, buff=1.0)
        self.play(FadeIn(conclusion, shift=UP*0.3), run_time=0.6)
        self.wait(1.0)

        # 1969 Minsky 著作
        book = Text("1969 · Minsky & Papert · 《Perceptrons》", font_size=22, color=GREY_B, font="Microsoft YaHei")
        book.to_edge(DOWN, buff=0.4)
        self.play(FadeOut(conclusion), FadeIn(book, shift=UP*0.2), run_time=0.6)
        self.wait(0.8)

        # AI 寒冬
        winter = make_zh("AI 寒冬 · 十几年无人问津", size=26, color=BLUE, weight=BOLD)
        winter.to_edge(DOWN, buff=0.4)
        self.play(FadeOut(book), FadeIn(winter, shift=UP*0.3), run_time=0.6)
        self.wait(2.0)
        self.wait(19.8)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


# =====================================================================
# S8: 多层突破
# =====================================================================
class S8_MultiLayer(Scene):
    def construct(self):
        title = make_zh("突破：叠一层", size=40, color=GOLD, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.8)
        self.wait(0.5)
        self.play(title.animate.scale(0.6).to_corner(UL, buff=0.3), run_time=0.4)

        # 三个门：NAND(上), OR(下), AND(右)
        x1 = Circle(radius=0.35, color=BLUE, fill_opacity=0.2, stroke_width=2).move_to(LEFT*5 + UP*1.2)
        x2 = Circle(radius=0.35, color=GREEN, fill_opacity=0.2, stroke_width=2).move_to(LEFT*5 + DOWN*1.2)
        x1t = Text("x₁", font_size=22, color=BLUE, font="Microsoft YaHei", weight=BOLD).move_to(x1)
        x2t = Text("x₂", font_size=22, color=GREEN, font="Microsoft YaHei", weight=BOLD).move_to(x2)

        nand = Circle(radius=0.5, color=PINK, fill_opacity=0.2, stroke_width=2.5).move_to(LEFT*1.5 + UP*1.2)
        or_g = Circle(radius=0.5, color=PURPLE, fill_opacity=0.2, stroke_width=2.5).move_to(LEFT*1.5 + DOWN*1.2)
        nand_t = Text("NAND", font_size=20, color=PINK, font="Consolas", weight=BOLD).move_to(nand)
        or_t = Text("OR", font_size=22, color=PURPLE, font="Consolas", weight=BOLD).move_to(or_g)

        and_g = Circle(radius=0.5, color=GOLD, fill_opacity=0.3, stroke_width=3).move_to(RIGHT*2.5)
        and_t = Text("AND", font_size=22, color=GOLD, font="Consolas", weight=BOLD).move_to(and_g)

        y_out = Circle(radius=0.4, color=WHITE, fill_opacity=0.2, stroke_width=2).move_to(RIGHT*5.5)
        y_t = Text("y", font_size=26, color=WHITE, font="Consolas", weight=BOLD).move_to(y_out)

        # 连线
        lines1 = VGroup(
            Line(x1.get_right(), nand.get_left() + UP*0.1, color=BLUE, stroke_width=2),
            Line(x2.get_right(), nand.get_left() + UP*0.1, color=GREEN, stroke_width=2),
            Line(x1.get_right(), or_g.get_left() + DOWN*0.1, color=BLUE, stroke_width=2),
            Line(x2.get_right(), or_g.get_left() + DOWN*0.1, color=GREEN, stroke_width=2),
        )
        lines2 = VGroup(
            Line(nand.get_right(), and_g.get_left() + UP*0.1, color=PINK, stroke_width=2),
            Line(or_g.get_right(), and_g.get_left() + DOWN*0.1, color=PURPLE, stroke_width=2),
        )
        line_out = Line(and_g.get_right(), y_out.get_left(), color=GOLD, stroke_width=2)

        # 层标签
        layer_lbls = VGroup(
            Text("Layer 0", font_size=18, color=GREY_C, font="Consolas").move_to(LEFT*5 + DOWN*3.0),
            Text("Layer 1", font_size=18, color=GREY_C, font="Consolas").move_to(LEFT*1.5 + DOWN*3.0),
            Text("Layer 2", font_size=18, color=GREY_C, font="Consolas").move_to(RIGHT*2.5 + DOWN*3.0),
        )

        # 构建
        self.play(GrowFromCenter(x1), GrowFromCenter(x2), FadeIn(x1t), FadeIn(x2t), run_time=0.5)
        self.play(Create(lines1), run_time=0.5)
        self.play(GrowFromCenter(nand), GrowFromCenter(or_g), FadeIn(nand_t), FadeIn(or_t), run_time=0.5)
        self.play(Create(lines2), run_time=0.4)
        self.play(GrowFromCenter(and_g), FadeIn(and_t), run_time=0.4)
        self.play(Create(line_out), GrowFromCenter(y_out), FadeIn(y_t), run_time=0.4)
        self.play(FadeIn(layer_lbls), run_time=0.4)
        self.wait(0.4)

        # 真值表
        truth_table = VGroup()
        header = Text("x₁  x₂  s₁  s₂  →  y", font_size=22, color=WHITE, font="Microsoft YaHei", weight=BOLD)
        header.move_to(RIGHT*2.5 + DOWN*0.5)
        truth_table.add(header)

        test_cases = [
            (0, 0, 1, 0, 0),
            (0, 1, 1, 1, 1),
            (1, 0, 1, 1, 1),
            (1, 1, 0, 1, 0),
        ]

        table_rows = []
        for i, (a, b, s1, s2, y) in enumerate(test_cases):
            row = Text(f" {a}    {b}    {s1}    {s2}    →   {y}",
                      font_size=20, color=GREY_B, font="Consolas")
            row.move_to(RIGHT*2.5 + DOWN*(1.0 + i*0.4))
            truth_table.add(row)
            table_rows.append(row)

        self.play(FadeIn(header), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(r) for r in table_rows], lag_ratio=0.15), run_time=0.8)
        self.wait(0.3)

        # 逐行验证
        for i, (a, b, s1, s2, y) in enumerate(test_cases):
            # 高亮当前行
            row_color = GREEN if y == (a ^ b) else RED_C
            self.play(table_rows[i].animate.set_color(GOLD), run_time=0.3)
            self.wait(0.2)

            # 模拟信号流
            if a: x1.set_fill(BLUE, opacity=0.8)
            if b: x2.set_fill(GREEN, opacity=0.8)
            nand.set_fill(PINK, opacity=0.7 if s1 else 0.2)
            or_g.set_fill(PURPLE, opacity=0.7 if s2 else 0.2)
            and_g.set_fill(GOLD, opacity=0.8 if y else 0.2)
            self.play(
                nand.animate.set_fill(PINK, opacity=0.7 if s1 else 0.2),
                or_g.animate.set_fill(PURPLE, opacity=0.7 if s2 else 0.2),
                and_g.animate.set_fill(GOLD, opacity=0.8 if y else 0.2),
                run_time=0.3
            )
            self.wait(0.2)

            # 打勾
            check = Text("✓", font_size=22, color=GREEN, font="Microsoft YaHei", weight=BOLD)
            check.next_to(table_rows[i], RIGHT, buff=0.15)
            self.play(FadeIn(check, scale=1.5), run_time=0.2)

            # 恢复
            self.play(
                table_rows[i].animate.set_color(GREEN),
                x1.animate.set_fill(BLUE, opacity=0.2),
                x2.animate.set_fill(GREEN, opacity=0.2),
                nand.animate.set_fill(PINK, opacity=0.2),
                or_g.animate.set_fill(PURPLE, opacity=0.2),
                and_g.animate.set_fill(GOLD, opacity=0.3),
                run_time=0.2
            )

        self.wait(0.8)
        # 总结
        summary = make_zh("单层做不到 · 加一层就搞定", size=26, color=GOLD, weight=BOLD)
        summary.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(summary, shift=UP*0.3), run_time=0.6)
        self.wait(1.5)
        self.wait(14.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


# =====================================================================
# S9: 流水线比喻
# =====================================================================
class S9_Pipeline(Scene):
    def construct(self):
        title = make_zh("流水线：每一层都在重新表达", size=32, color=WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.6)
        self.wait(0.3)
        self.play(title.animate.scale(0.6).to_edge(UP, buff=0.2), run_time=0.4)

        # 简化的多层网络
        # Layer 0: 2个输入
        l0 = VGroup()
        for i, col in enumerate([BLUE, GREEN]):
            c = Circle(radius=0.3, color=col, fill_opacity=0.2, stroke_width=2)
            c.move_to(LEFT*5 + UP*(0.5 - i))
            t = Text("x" + str(i+1), font_size=18, color=col, font="Consolas", weight=BOLD).move_to(c)
            l0.add(VGroup(c, t))

        # Layer 1: 4个神经元
        l1 = VGroup()
        cols1 = [PINK, PURPLE, TEAL, ORANGE]
        for i, col in enumerate(cols1):
            c = Circle(radius=0.3, color=col, fill_opacity=0.2, stroke_width=2)
            c.move_to(LEFT*1.5 + UP*(1.5 - i))
            t = Text(f"h₁{i+1}", font_size=16, color=col, font="Microsoft YaHei", weight=BOLD).move_to(c)
            l1.add(VGroup(c, t))

        # Layer 2: 3个神经元
        l2 = VGroup()
        cols2 = [GOLD, GREEN, BLUE]
        for i, col in enumerate(cols2):
            c = Circle(radius=0.3, color=col, fill_opacity=0.2, stroke_width=2)
            c.move_to(RIGHT*2 + UP*(1.0 - i))
            t = Text(f"h₂{i+1}", font_size=16, color=col, font="Microsoft YaHei", weight=BOLD).move_to(c)
            l2.add(VGroup(c, t))

        # Layer 3: 1个输出
        l3 = VGroup()
        c = Circle(radius=0.3, color=WHITE, fill_opacity=0.2, stroke_width=2)
        c.move_to(RIGHT*5)
        t = Text("y", font_size=22, color=WHITE, font="Consolas", weight=BOLD).move_to(c)
        l3.add(VGroup(c, t))

        # 全部连接 (简化：每层都连)
        all_lines = VGroup()
        for src in l0:
            for dst in l1:
                all_lines.add(Line(src[0].get_right(), dst[0].get_left(),
                                   color=GREY_D, stroke_width=1).set_opacity(0.5))
        for src in l1:
            for dst in l2:
                all_lines.add(Line(src[0].get_right(), dst[0].get_left(),
                                   color=GREY_D, stroke_width=1).set_opacity(0.5))
        for src in l2:
            for dst in l3:
                all_lines.add(Line(src[0].get_right(), dst[0].get_left(),
                                   color=GREY_D, stroke_width=1).set_opacity(0.5))

        # 标签
        lbls = VGroup(
            Text("Layer 0", font_size=18, color=GREY_C, font="Consolas").move_to(LEFT*5 + DOWN*2.8),
            Text("Layer 1", font_size=18, color=GREY_C, font="Consolas").move_to(LEFT*1.5 + DOWN*2.8),
            Text("Layer 2", font_size=18, color=GREY_C, font="Consolas").move_to(RIGHT*2 + DOWN*2.8),
            Text("Layer 3", font_size=18, color=GREY_C, font="Consolas").move_to(RIGHT*5 + DOWN*2.8),
        )

        # 顺序：连线 → 节点
        self.play(LaggedStart(*[Create(l) for l in all_lines], lag_ratio=0.005), run_time=2.0)
        self.play(FadeIn(l0), FadeIn(l1), FadeIn(l2), FadeIn(l3), run_time=0.6)
        self.play(FadeIn(lbls), run_time=0.4)
        self.wait(0.5)

        # 信号流动画 - 沿网络传送
        for stage in range(3):
            # 激活当前层
            if stage == 0:
                targets = l0
            elif stage == 1:
                targets = l1
            elif stage == 2:
                targets = l2
            for c in targets:
                c[0].set_fill(c[0].get_color(), opacity=0.8)
            self.play(*[c[0].animate.set_fill(c[0].get_color(), opacity=0.8) for c in targets], run_time=0.3)
            self.wait(0.1)
            self.play(*[c[0].animate.set_fill(c[0].get_color(), opacity=0.2) for c in targets], run_time=0.3)

        # 总结
        summary1 = make_zh("每一层 = 一次加工", size=24, color=GOLD, weight=BOLD)
        summary1.move_to(UP*2.2)
        summary2 = make_zh("组合特征 · 层层抽象", size=20, color=GREY_B)
        summary2.move_to(UP*1.7)
        self.play(FadeIn(summary1, shift=UP*0.3), run_time=0.5)
        self.play(FadeIn(summary2, shift=UP*0.2), run_time=0.5)
        self.wait(2.0)
        self.wait(15.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


# =====================================================================
# S10: 从 NAND 到计算机
# =====================================================================
class S10_NAND(Scene):
    def construct(self):
        title = make_zh("从 NAND 到计算机", size=36, color=WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.6)
        self.wait(0.3)
        self.play(title.animate.scale(0.65).to_edge(UP, buff=0.2), run_time=0.4)

        # 中央链条
        stages = [
            ("NAND", PINK, 0),
            ("NOT", TEAL, 1),
            ("AND / OR", BLUE, 2),
            ("半加器", PURPLE, 3),
            ("全加器", ORANGE, 4),
            ("ALU", GREEN, 5),
            ("CPU", GOLD, 6),
            ("计算机", WHITE, 7),
        ]

        # 链条节点
        nodes = VGroup()
        for i, (name, col, _) in enumerate(stages):
            box = RoundedRectangle(width=1.4, height=0.7, corner_radius=0.08,
                                   fill_color=GREY_E, fill_opacity=0.7,
                                   stroke_color=col, stroke_width=2)
            t = Text(name, font_size=18, color=col, font="Microsoft YaHei", weight=BOLD).move_to(box)
            nodes.add(VGroup(box, t))

        nodes.arrange(DOWN, buff=0.25)
        nodes.move_to(LEFT*3 + DOWN*0.2)

        # 链条箭头
        arrows = VGroup()
        for i in range(len(nodes) - 1):
            arr = Arrow(nodes[i].get_bottom(), nodes[i+1].get_top(),
                       buff=0.08, color=GREY_C, stroke_width=1.5, max_tip_length_to_length_ratio=0.3)
            arrows.add(arr)

        # 右侧：每一级的展开说明
        notes = VGroup()
        notes_data = [
            "用感知机实现",
            "NAND + 组合",
            "基本逻辑门",
            "XOR + AND",
            "两个半加器",
            "加法 + 选择",
            "指令 + 控制",
            "内存 + IO"
        ]
        for i, note in enumerate(notes_data):
            t = Text(note, font_size=18, color=GREY_B, font="Microsoft YaHei")
            t.move_to(RIGHT*3 + UP*(2.5 - i*0.6))
            notes.add(t)

        # 逐级显示
        for i, (node_group, arrow) in enumerate(zip(nodes, [None] + list(arrows))):
            self.play(FadeIn(node_group, shift=UP*0.2), run_time=0.4)
            if arrow:
                self.play(Create(arrow), run_time=0.25)
            self.play(FadeIn(notes[i], shift=LEFT*0.2), run_time=0.3)
            self.wait(0.15)

        self.wait(0.5)

        # 强调
        em = make_zh("NAND 堆起来 = 一台计算机", size=28, color=GOLD, weight=BOLD)
        em.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(em, shift=UP*0.3), run_time=0.6)
        self.wait(1.5)

        # 进阶
        sub = make_zh("参考《计算机系统要素：从零开始构建现代计算机》",
                     size=16, color=GREY_C)
        sub.to_edge(DOWN, buff=0.2)
        self.play(FadeOut(em), FadeIn(sub), run_time=0.4)
        self.wait(1.5)
        self.wait(23.7)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


# =====================================================================
# S11: 通用逼近定理
# =====================================================================
class S11_Universal(Scene):
    def construct(self):
        title = make_zh("通用逼近定理：2 层就够", size=32, color=WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.6)
        self.wait(0.3)
        self.play(title.animate.scale(0.6).to_edge(UP, buff=0.2), run_time=0.4)

        # 公式
        formula = Text("2层感知机 + 非线性激活  →  任意函数",
                      font_size=30, color=GOLD, font="Microsoft YaHei", weight=BOLD)
        formula.shift(UP*1.5)
        self.play(Write(formula), run_time=1.0)
        self.wait(0.5)

        # 坐标系
        axes = Axes(
            x_range=[-3, 3, 1], y_range=[-1.5, 1.5, 1],
            x_length=6, y_length=3,
            axis_config={"color": GREY_D, "stroke_width": 1.2},
        ).shift(DOWN*0.8)
        x_lbl = Text("x", font_size=18, color=WHITE, font="Consolas").next_to(axes.x_axis, RIGHT, buff=0.15)

        # 目标函数：sin(x)
        target = axes.plot(lambda x: np.sin(x), x_range=[-3, 3], color=WHITE, stroke_width=3)
        target_lbl = Text("sin(x)", font_size=20, color=WHITE, font="Consolas").next_to(target, UP, buff=0.1).shift(LEFT*2)
        self.play(Create(axes), FadeIn(x_lbl), run_time=0.6)
        self.play(Create(target), FadeIn(target_lbl), run_time=0.8)
        self.wait(0.3)

        # 阶梯函数近似
        steps = 5
        approx = VGroup()
        for i in range(steps):
            x0 = -3 + i * 6 / steps
            x1 = -3 + (i+1) * 6 / steps
            y_val = np.sin((x0 + x1) / 2)
            seg = Line(axes.c2p(x0, y_val), axes.c2p(x1, y_val),
                      color=ORANGE, stroke_width=3)
            approx.add(seg)
        self.play(LaggedStart(*[Create(s) for s in approx], lag_ratio=0.1), run_time=0.8)
        self.wait(0.3)

        # 更多阶梯 → 更精确
        for steps in [10, 20, 40]:
            new_approx = VGroup()
            for i in range(steps):
                x0 = -3 + i * 6 / steps
                x1 = -3 + (i+1) * 6 / steps
                y_val = np.sin((x0 + x1) / 2)
                seg = Line(axes.c2p(x0, y_val), axes.c2p(x1, y_val),
                          color=ORANGE, stroke_width=2)
                new_approx.add(seg)
            self.play(Transform(approx, new_approx), run_time=0.4)
            self.wait(0.2)

        # 强调
        em = make_zh("2 层够用 · 但工程上要更深", size=24, color=GOLD, weight=BOLD)
        em.next_to(axes, DOWN, buff=0.4)
        self.play(FadeIn(em, shift=UP*0.3), run_time=0.6)
        self.wait(2.0)
        self.wait(18.3)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


# =====================================================================
# S12: 升华与下期
# =====================================================================
class S12_Ending(Scene):
    def construct(self):
        # 黑屏
        self.wait(0.5)

        # 单感知机浮现
        x1 = Circle(radius=0.3, color=BLUE, fill_opacity=0.3, stroke_width=2).move_to(LEFT*2 + UP*2)
        x2 = Circle(radius=0.3, color=GREEN, fill_opacity=0.3, stroke_width=2).move_to(LEFT*2 + DOWN*0.5)
        neuron = Circle(radius=0.5, color=GOLD, fill_opacity=0.3, stroke_width=2.5).move_to(LEFT*2)
        L1 = Line(x1.get_right(), neuron.get_left() + UP*0.15, color=BLUE, stroke_width=2)
        L2 = Line(x2.get_right(), neuron.get_left() + DOWN*0.15, color=GREEN, stroke_width=2)
        ar = Arrow(neuron.get_right(), RIGHT*0.3, color=GOLD, stroke_width=2)
        per = make_zh("感知机", size=22, color=WHITE)
        per.next_to(neuron, DOWN, buff=0.6)

        self.play(
            GrowFromCenter(x1), GrowFromCenter(x2),
            Create(L1), Create(L2),
            GrowFromCenter(neuron),
            run_time=0.8
        )
        self.play(GrowArrow(ar), FadeIn(per), run_time=0.4)
        self.wait(1.0)

        # 时间回溯标签
        year = Text("1957", font_size=28, color=GOLD, font="Consolas", weight=BOLD)
        year.to_edge(LEFT, buff=0.5).shift(DOWN*1.5)
        self.play(FadeIn(year), run_time=0.4)
        self.wait(0.5)

        # 演化：网络扩大
        layers_added = []
        for k in range(3):
            new_layer = VGroup()
            for j, col in enumerate([BLUE, GREEN, PINK]):
                c = Circle(radius=0.25, color=col, fill_opacity=0.3, stroke_width=2)
                c.move_to(RIGHT*2.5 + UP*(1.0 - j*1.0) + RIGHT*k*0.0)
                new_layer.add(c)
            new_layer.move_to(RIGHT*(2 + k*1.5))
            layers_added.append(new_layer)

        # 渐次出现
        for layer in layers_added:
            self.play(FadeIn(layer, lag_ratio=0.1), run_time=0.4)
            self.wait(0.2)

        self.wait(0.5)

        # 全部转成更复杂的网络 - 简化表示
        complex_net_text = make_zh("一层 → 多层 → 任意网络", size=28, color=GOLD, weight=BOLD)
        complex_net_text.move_to(DOWN*0.5)
        self.play(FadeIn(complex_net_text, shift=UP*0.3), run_time=0.6)
        self.wait(0.5)

        # 中心标题
        main = Text("1957", font_size=80, color=GOLD, font="Consolas", weight=BOLD)
        main.move_to(DOWN*1.8)
        self.play(FadeIn(main, shift=UP*0.3), run_time=0.6)
        self.wait(0.3)

        sub1 = make_zh("深度学习最底层的故事", size=24, color=WHITE, weight=BOLD)
        sub1.next_to(main, DOWN, buff=0.4)
        self.play(FadeIn(sub1, shift=UP*0.2), run_time=0.5)
        self.wait(0.3)

        sub2 = make_zh("下一章 · 从感知机到神经网络", size=20, color=BLUE)
        sub2.next_to(sub1, DOWN, buff=0.3)
        self.play(FadeIn(sub2, shift=UP*0.2), run_time=0.5)
        self.wait(3.0)
        self.wait(25.2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
