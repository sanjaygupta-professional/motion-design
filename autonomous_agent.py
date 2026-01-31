"""
Autonomous Agent Visualization with Manim
==========================================
This script creates animated visualizations explaining how autonomous coding agents work.

Scenes:
1. CompoundLoopScene - The core loop: report → PRD → tasks → implementation → PR
2. TaskDecompositionScene - How agents break down work into small tasks
3. KnowledgeCompoundingScene - How CLAUDE.md grows smarter over time
4. NightlyWorkflowScene - The two-phase nightly process
5. FullExplainerScene - Complete walkthrough combining all concepts

Author: Created with Claude Code assistance
Purpose: Educational content for understanding autonomous coding agents
"""

from manim import *
import numpy as np


# Color palette
COLORS = {
    "primary": "#6366F1",      # Indigo
    "secondary": "#8B5CF6",    # Purple
    "accent": "#10B981",       # Emerald
    "warning": "#F59E0B",      # Amber
    "background": "#1E1E2E",   # Dark
    "text": "#E2E8F0",         # Light gray
    "success": "#22C55E",      # Green
    "code": "#3B82F6",         # Blue
}


class CompoundLoopScene(Scene):
    """
    Visualizes the core compound engineering loop:
    Report → PRD → Tasks → Implementation → PR
    """

    def construct(self):
        self.camera.background_color = COLORS["background"]

        # Title
        title = Text("The Compound Engineering Loop", font_size=40, color=COLORS["text"])
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)

        # Create the circular flow
        center = ORIGIN
        radius = 2.2

        # Nodes in the loop
        nodes_data = [
            ("📋 Report", "Your priorities", 90),
            ("📝 PRD", "Requirements doc", 18),
            ("✅ Tasks", "User stories", -54),
            ("💻 Implement", "Code changes", -126),
            ("🔀 PR", "Pull request", -198),
        ]

        nodes = []
        labels = []
        sublabels = []

        for text, subtext, angle in nodes_data:
            # Calculate position
            rad = angle * DEGREES
            pos = center + radius * np.array([np.cos(rad), np.sin(rad), 0])

            # Create node
            node = RoundedRectangle(
                corner_radius=0.2,
                width=1.8,
                height=0.9,
                fill_color=COLORS["primary"],
                fill_opacity=0.8,
                stroke_color=COLORS["secondary"],
                stroke_width=2
            ).move_to(pos)

            label = Text(text, font_size=20, color=WHITE).move_to(pos + UP * 0.1)
            sublabel = Text(subtext, font_size=12, color=COLORS["text"]).move_to(pos + DOWN * 0.25)

            nodes.append(node)
            labels.append(label)
            sublabels.append(sublabel)

        # Animate nodes appearing
        self.play(
            LaggedStart(*[
                AnimationGroup(
                    GrowFromCenter(node),
                    FadeIn(label),
                    FadeIn(sublabel)
                )
                for node, label, sublabel in zip(nodes, labels, sublabels)
            ], lag_ratio=0.2),
            run_time=2.5
        )

        # Create arrows between nodes
        arrows = []
        for i in range(len(nodes)):
            start_node = nodes[i]
            end_node = nodes[(i + 1) % len(nodes)]

            # Calculate arrow positions
            start = start_node.get_center()
            end = end_node.get_center()
            direction = end - start
            direction = direction / np.linalg.norm(direction)

            arrow = Arrow(
                start + direction * 0.95,
                end - direction * 0.95,
                color=COLORS["accent"],
                buff=0,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.15
            )
            arrows.append(arrow)

        self.play(
            LaggedStart(*[GrowArrow(arrow) for arrow in arrows], lag_ratio=0.15),
            run_time=1.5
        )

        # Animate the flow
        dot = Dot(color=COLORS["warning"], radius=0.15)
        dot.move_to(nodes[0].get_center())
        self.play(FadeIn(dot, scale=0.5))

        # Move dot around the loop twice
        for _ in range(2):
            for i in range(len(nodes)):
                next_idx = (i + 1) % len(nodes)
                # Highlight current node
                self.play(
                    nodes[i].animate.set_fill(COLORS["accent"], opacity=0.9),
                    run_time=0.2
                )
                self.play(
                    dot.animate.move_to(nodes[next_idx].get_center()),
                    nodes[i].animate.set_fill(COLORS["primary"], opacity=0.8),
                    run_time=0.4
                )

        self.play(FadeOut(dot))

        # Add "Repeat Nightly" text
        repeat_text = Text("↻ Repeats Every Night", font_size=24, color=COLORS["accent"])
        repeat_text.next_to(center, DOWN, buff=0.3)
        self.play(Write(repeat_text))

        self.wait(2)


class TaskDecompositionScene(Scene):
    """
    Shows how a high-level task gets broken into small, testable user stories.
    """

    def construct(self):
        self.camera.background_color = COLORS["background"]

        # Title
        title = Text("Task Decomposition", font_size=40, color=COLORS["text"])
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))

        # Big task (the report priority)
        big_task = VGroup(
            RoundedRectangle(
                corner_radius=0.2, width=6, height=1.2,
                fill_color=COLORS["warning"], fill_opacity=0.8,
                stroke_color=WHITE, stroke_width=2
            ),
            Text("Add cross-references to learning path", font_size=18, color=WHITE)
        )
        big_task[1].move_to(big_task[0].get_center())
        big_task.move_to(UP * 1.5)

        self.play(GrowFromCenter(big_task))
        self.wait(0.5)

        # Arrow down
        arrow_down = Arrow(
            big_task.get_bottom() + DOWN * 0.2,
            big_task.get_bottom() + DOWN * 1,
            color=COLORS["accent"],
            stroke_width=3
        )

        agent_label = Text("Agent analyzes & breaks down", font_size=14, color=COLORS["text"])
        agent_label.next_to(arrow_down, RIGHT, buff=0.3)

        self.play(GrowArrow(arrow_down), FadeIn(agent_label))

        # Small tasks
        small_tasks_data = [
            ("1. Add Related Concepts", "Links to /concepts/ pages"),
            ("2. Add Go Deeper sections", "Optional reading links"),
            ("3. Enhance Path Complete", "Summary + verification"),
        ]

        small_tasks = VGroup()
        for i, (task_title, task_desc) in enumerate(small_tasks_data):
            task = VGroup(
                RoundedRectangle(
                    corner_radius=0.15, width=3.5, height=0.9,
                    fill_color=COLORS["primary"], fill_opacity=0.8,
                    stroke_color=COLORS["secondary"], stroke_width=2
                ),
                Text(task_title, font_size=14, color=WHITE),
                Text(task_desc, font_size=10, color=COLORS["text"])
            )
            task[1].move_to(task[0].get_center() + UP * 0.15)
            task[2].move_to(task[0].get_center() + DOWN * 0.2)
            small_tasks.add(task)

        small_tasks.arrange(RIGHT, buff=0.3)
        small_tasks.move_to(DOWN * 1.2)

        self.play(
            LaggedStart(*[GrowFromCenter(task) for task in small_tasks], lag_ratio=0.2),
            run_time=1.5
        )

        # Add checkmarks one by one
        checks = []
        for i, task in enumerate(small_tasks):
            check = Text("✓", font_size=28, color=COLORS["success"])
            check.move_to(task[0].get_corner(UR) + LEFT * 0.3 + DOWN * 0.2)
            checks.append(check)

        self.wait(0.5)
        for i, check in enumerate(checks):
            self.play(
                FadeIn(check, scale=2),
                small_tasks[i][0].animate.set_stroke(COLORS["success"], width=3),
                run_time=0.4
            )
            self.wait(0.3)

        # Final message
        message = Text(
            "Each task: Small, testable, independently completable",
            font_size=18,
            color=COLORS["accent"]
        )
        message.to_edge(DOWN, buff=0.8)
        self.play(Write(message))

        self.wait(2)


class KnowledgeCompoundingScene(Scene):
    """
    Shows how CLAUDE.md grows smarter over time as the agent learns.
    """

    def construct(self):
        self.camera.background_color = COLORS["background"]

        # Title
        title = Text("Knowledge Compounding", font_size=40, color=COLORS["text"])
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))

        # CLAUDE.md file representation
        file_box = VGroup(
            RoundedRectangle(
                corner_radius=0.1, width=4, height=5,
                fill_color="#2D2D3D", fill_opacity=1,
                stroke_color=COLORS["code"], stroke_width=2
            ),
            Text("CLAUDE.md", font_size=16, color=COLORS["code"])
        )
        file_box[1].move_to(file_box[0].get_top() + DOWN * 0.3)
        file_box.move_to(LEFT * 3)

        self.play(GrowFromCenter(file_box))

        # Initial content
        initial_content = VGroup(
            Text("## Project Overview", font_size=12, color=WHITE),
            Text("Tech stack, structure...", font_size=10, color=GRAY),
            Text("", font_size=10),
            Text("## Patterns Discovered", font_size=12, color=WHITE),
            Text("(empty)", font_size=10, color=GRAY),
            Text("", font_size=10),
            Text("## Gotchas", font_size=12, color=WHITE),
            Text("(empty)", font_size=10, color=GRAY),
        )
        initial_content.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        initial_content.move_to(file_box[0].get_center() + DOWN * 0.3)
        initial_content.scale(0.9)

        self.play(FadeIn(initial_content))

        # Timeline on the right
        timeline_title = Text("Time →", font_size=14, color=COLORS["text"])
        timeline_title.move_to(RIGHT * 2 + UP * 2)
        self.play(Write(timeline_title))

        # Days and learnings
        days_data = [
            ("Day 1", "Pattern: Use h3 for subsections"),
            ("Day 2", "Gotcha: Mermaid needs code blocks"),
            ("Day 3", "Pattern: Progressive disclosure"),
            ("Day 4", "Gotcha: Build before commit"),
            ("Day 5", "Pattern: Consistent link format"),
        ]

        days = VGroup()
        for i, (day, learning) in enumerate(days_data):
            day_group = VGroup(
                Dot(color=COLORS["accent"], radius=0.1),
                Text(day, font_size=12, color=WHITE),
                Text(learning, font_size=10, color=COLORS["text"])
            )
            day_group[1].next_to(day_group[0], RIGHT, buff=0.15)
            day_group[2].next_to(day_group[1], DOWN, aligned_edge=LEFT, buff=0.05)
            days.add(day_group)

        days.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        days.move_to(RIGHT * 2.5 + DOWN * 0.3)

        # Animate days appearing and knowledge growing
        # Create growing content items
        new_patterns = [
            Text("• h3 for subsections", font_size=9, color=COLORS["accent"]),
            Text("• Progressive disclosure", font_size=9, color=COLORS["accent"]),
            Text("• Consistent link format", font_size=9, color=COLORS["accent"]),
        ]

        new_gotchas = [
            Text("• Mermaid needs code blocks", font_size=9, color=COLORS["warning"]),
            Text("• Build before commit", font_size=9, color=COLORS["warning"]),
        ]

        pattern_idx = 0
        gotcha_idx = 0

        for i, day_group in enumerate(days):
            # Show the day
            self.play(FadeIn(day_group, shift=LEFT * 0.3), run_time=0.4)

            # Arrow from day to file
            arrow = Arrow(
                day_group.get_left() + LEFT * 0.2,
                file_box[0].get_right() + RIGHT * 0.1,
                color=COLORS["accent"],
                stroke_width=2,
                max_tip_length_to_length_ratio=0.1
            )
            self.play(GrowArrow(arrow), run_time=0.3)

            # Add content to file based on type
            learning = days_data[i][1]
            if "Pattern" in learning and pattern_idx < len(new_patterns):
                new_patterns[pattern_idx].next_to(
                    initial_content[4] if pattern_idx == 0 else new_patterns[pattern_idx-1],
                    DOWN, aligned_edge=LEFT, buff=0.05
                )
                self.play(FadeIn(new_patterns[pattern_idx], shift=UP * 0.1), run_time=0.3)
                pattern_idx += 1
            elif "Gotcha" in learning and gotcha_idx < len(new_gotchas):
                new_gotchas[gotcha_idx].next_to(
                    initial_content[7] if gotcha_idx == 0 else new_gotchas[gotcha_idx-1],
                    DOWN, aligned_edge=LEFT, buff=0.05
                )
                self.play(FadeIn(new_gotchas[gotcha_idx], shift=UP * 0.1), run_time=0.3)
                gotcha_idx += 1

            self.play(FadeOut(arrow), run_time=0.2)

        # Final message
        message = VGroup(
            Text("Agent gets smarter", font_size=20, color=COLORS["success"]),
            Text("every single day", font_size=20, color=COLORS["success"])
        )
        message.arrange(DOWN, buff=0.1)
        message.to_edge(DOWN, buff=0.6)
        self.play(Write(message))

        self.wait(2)


class NightlyWorkflowScene(Scene):
    """
    Shows the two-phase nightly process: Review (10:30 PM) → Auto-Compound (11:00 PM)
    """

    def construct(self):
        self.camera.background_color = COLORS["background"]

        # Title
        title = Text("The Nightly Workflow", font_size=40, color=COLORS["text"])
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))

        # Timeline
        timeline = Line(LEFT * 5, RIGHT * 5, color=COLORS["text"], stroke_width=2)
        timeline.move_to(ORIGIN)
        self.play(Create(timeline))

        # Time markers
        times = [
            (LEFT * 4, "10:30 PM"),
            (LEFT * 1, "11:00 PM"),
            (RIGHT * 2.5, "Morning"),
        ]

        time_markers = VGroup()
        for pos, label in times:
            marker = VGroup(
                Line(pos + UP * 0.15, pos + DOWN * 0.15, color=WHITE, stroke_width=2),
                Text(label, font_size=14, color=COLORS["text"])
            )
            marker[1].next_to(marker[0], DOWN, buff=0.1)
            time_markers.add(marker)

        self.play(LaggedStart(*[FadeIn(m) for m in time_markers], lag_ratio=0.2))

        # Phase 1: Compound Review
        phase1 = VGroup(
            RoundedRectangle(
                corner_radius=0.15, width=2.8, height=2,
                fill_color=COLORS["secondary"], fill_opacity=0.7,
                stroke_color=WHITE, stroke_width=2
            ),
            Text("🔍 Review", font_size=18, color=WHITE),
            Text("• Read git log", font_size=11, color=COLORS["text"]),
            Text("• Extract learnings", font_size=11, color=COLORS["text"]),
            Text("• Update CLAUDE.md", font_size=11, color=COLORS["text"]),
        )
        phase1[1].move_to(phase1[0].get_top() + DOWN * 0.35)
        content1 = VGroup(phase1[2], phase1[3], phase1[4])
        content1.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        content1.move_to(phase1[0].get_center() + DOWN * 0.2)
        phase1.move_to(LEFT * 4 + UP * 1.8)

        self.play(GrowFromCenter(phase1))

        # Arrow to phase 2
        arrow1 = Arrow(
            phase1.get_right() + RIGHT * 0.1,
            LEFT * 1 + UP * 1.8 + LEFT * 1.4,
            color=COLORS["accent"],
            stroke_width=3
        )
        self.play(GrowArrow(arrow1))

        # Phase 2: Auto-Compound
        phase2 = VGroup(
            RoundedRectangle(
                corner_radius=0.15, width=2.8, height=2.4,
                fill_color=COLORS["primary"], fill_opacity=0.7,
                stroke_color=WHITE, stroke_width=2
            ),
            Text("🚀 Implement", font_size=18, color=WHITE),
            Text("• Read report", font_size=11, color=COLORS["text"]),
            Text("• Create PRD", font_size=11, color=COLORS["text"]),
            Text("• Execute tasks", font_size=11, color=COLORS["text"]),
            Text("• Create PR", font_size=11, color=COLORS["text"]),
        )
        phase2[1].move_to(phase2[0].get_top() + DOWN * 0.35)
        content2 = VGroup(phase2[2], phase2[3], phase2[4], phase2[5])
        content2.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        content2.move_to(phase2[0].get_center() + DOWN * 0.15)
        phase2.move_to(LEFT * 1 + UP * 1.8)

        self.play(GrowFromCenter(phase2))

        # Arrow to result
        arrow2 = Arrow(
            phase2.get_right() + RIGHT * 0.1,
            RIGHT * 2.5 + UP * 1.8 + LEFT * 1.2,
            color=COLORS["accent"],
            stroke_width=3
        )
        self.play(GrowArrow(arrow2))

        # Result: Morning
        result = VGroup(
            RoundedRectangle(
                corner_radius=0.15, width=2.8, height=1.8,
                fill_color=COLORS["success"], fill_opacity=0.7,
                stroke_color=WHITE, stroke_width=2
            ),
            Text("☀️ You Wake Up", font_size=18, color=WHITE),
            Text("• PR ready to review", font_size=11, color=COLORS["text"]),
            Text("• Smarter CLAUDE.md", font_size=11, color=COLORS["text"]),
        )
        result[1].move_to(result[0].get_top() + DOWN * 0.35)
        content3 = VGroup(result[2], result[3])
        content3.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        content3.move_to(result[0].get_center() + DOWN * 0.15)
        result.move_to(RIGHT * 2.5 + UP * 1.8)

        self.play(GrowFromCenter(result))

        # Bottom message
        message = Text(
            "Order matters: Review updates CLAUDE.md → Implementation benefits from learnings",
            font_size=14,
            color=COLORS["accent"]
        )
        message.to_edge(DOWN, buff=0.6)
        self.play(Write(message))

        self.wait(2)


class FullExplainerScene(Scene):
    """
    Complete walkthrough of the autonomous agent system.
    Combines all concepts into one cohesive narrative.
    """

    def construct(self):
        self.camera.background_color = COLORS["background"]

        # Scene 1: Title
        title = Text("Autonomous Coding Agents", font_size=48, color=WHITE)
        subtitle = Text("How AI ships code while you sleep", font_size=24, color=COLORS["accent"])
        subtitle.next_to(title, DOWN, buff=0.3)

        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle, shift=UP * 0.2))
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle))

        # Scene 2: The Problem
        problem_title = Text("The Traditional Workflow", font_size=32, color=COLORS["text"])
        problem_title.to_edge(UP, buff=0.8)
        self.play(Write(problem_title))

        # Human working icon
        human = VGroup(
            Circle(radius=0.3, color=COLORS["warning"], fill_opacity=0.8),
            Text("👨‍💻", font_size=36)
        )
        human[1].move_to(human[0].get_center())
        human.move_to(LEFT * 2)

        # Arrow to code
        work_arrow = Arrow(LEFT * 1, RIGHT * 1, color=WHITE, stroke_width=2)

        # Code icon
        code = VGroup(
            RoundedRectangle(width=1.5, height=1, corner_radius=0.1,
                           fill_color=COLORS["code"], fill_opacity=0.8),
            Text("{ }", font_size=24, color=WHITE)
        )
        code[1].move_to(code[0].get_center())
        code.move_to(RIGHT * 2)

        self.play(FadeIn(human), GrowArrow(work_arrow), FadeIn(code))

        # "Only during work hours" text
        work_hours = Text("Only during work hours", font_size=18, color=COLORS["warning"])
        work_hours.next_to(work_arrow, DOWN, buff=0.3)
        self.play(Write(work_hours))

        self.wait(1)

        # Clock showing night - work stops
        night_text = Text("🌙 Night = No progress", font_size=20, color=GRAY)
        night_text.to_edge(DOWN, buff=1)
        self.play(Write(night_text))

        self.wait(1)
        self.play(
            FadeOut(problem_title), FadeOut(human), FadeOut(work_arrow),
            FadeOut(code), FadeOut(work_hours), FadeOut(night_text)
        )

        # Scene 3: The Solution
        solution_title = Text("The Compound Engineering Way", font_size=32, color=COLORS["accent"])
        solution_title.to_edge(UP, buff=0.8)
        self.play(Write(solution_title))

        # Day: Human + Agent
        day_group = VGroup(
            Text("☀️ Day", font_size=20, color=WHITE),
            Text("You work + Agent learns", font_size=14, color=COLORS["text"])
        )
        day_group.arrange(DOWN, buff=0.1)
        day_group.move_to(LEFT * 3)

        # Night: Agent works
        night_group = VGroup(
            Text("🌙 Night", font_size=20, color=WHITE),
            Text("Agent implements priorities", font_size=14, color=COLORS["text"])
        )
        night_group.arrange(DOWN, buff=0.1)
        night_group.move_to(ORIGIN)

        # Morning: PR ready
        morning_group = VGroup(
            Text("☀️ Morning", font_size=20, color=WHITE),
            Text("PR ready + smarter agent", font_size=14, color=COLORS["text"])
        )
        morning_group.arrange(DOWN, buff=0.1)
        morning_group.move_to(RIGHT * 3)

        # Arrows
        arrow1 = Arrow(day_group.get_right(), night_group.get_left(), color=COLORS["accent"])
        arrow2 = Arrow(night_group.get_right(), morning_group.get_left(), color=COLORS["accent"])

        self.play(
            FadeIn(day_group),
            FadeIn(night_group),
            FadeIn(morning_group),
            GrowArrow(arrow1),
            GrowArrow(arrow2)
        )

        # Highlight: 24/7 progress
        progress_text = Text("✨ Progress 24/7 ✨", font_size=24, color=COLORS["success"])
        progress_text.to_edge(DOWN, buff=1)
        self.play(Write(progress_text))

        self.wait(1.5)
        self.play(
            FadeOut(solution_title), FadeOut(day_group), FadeOut(night_group),
            FadeOut(morning_group), FadeOut(arrow1), FadeOut(arrow2), FadeOut(progress_text)
        )

        # Scene 4: Key Insight
        insight_title = Text("The Key Insight", font_size=36, color=WHITE)
        insight_title.move_to(UP * 2)

        insight_text = Text(
            "Each unit of work should make\nsubsequent work easier",
            font_size=24,
            color=COLORS["accent"],
            line_spacing=1.5
        )
        insight_text.move_to(ORIGIN)

        self.play(Write(insight_title))
        self.play(Write(insight_text), run_time=2)

        # Compound effect visualization
        compound = VGroup(
            Text("Day 1: Agent learns patterns", font_size=16, color=COLORS["text"]),
            Text("Day 2: Agent avoids past mistakes", font_size=16, color=COLORS["text"]),
            Text("Day 3: Agent follows conventions", font_size=16, color=COLORS["text"]),
            Text("Day N: Agent knows your codebase", font_size=16, color=COLORS["success"]),
        )
        compound.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        compound.move_to(DOWN * 1.5)

        self.play(
            LaggedStart(*[FadeIn(line, shift=RIGHT * 0.3) for line in compound], lag_ratio=0.3),
            run_time=2
        )

        self.wait(2)

        # Final frame
        self.play(*[FadeOut(mob) for mob in self.mobjects])

        final = VGroup(
            Text("Stop Prompting.", font_size=36, color=WHITE),
            Text("Start Compounding.", font_size=36, color=COLORS["accent"])
        )
        final.arrange(DOWN, buff=0.3)

        self.play(Write(final), run_time=2)
        self.wait(2)


# To render, run:
# manim -pql autonomous_agent.py CompoundLoopScene
# manim -pql autonomous_agent.py TaskDecompositionScene
# manim -pql autonomous_agent.py KnowledgeCompoundingScene
# manim -pql autonomous_agent.py NightlyWorkflowScene
# manim -pql autonomous_agent.py FullExplainerScene
#
# For high quality:
# manim -pqh autonomous_agent.py FullExplainerScene
