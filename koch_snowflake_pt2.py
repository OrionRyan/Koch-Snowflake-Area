from manim import *

class Delta(Scene):
    def construct(self):

        aspect_ratio = Rectangle(width=4.5, height=8, color=WHITE)
        self.add(aspect_ratio)

        #Function to remove stray braces
        #(just a modified version of an already existing method within manim)
        def remove_stray_braces(tex):
            num_lefts = tex.get_tex_string().count("{")
            num_rights = tex.get_tex_string().count("}")
            while num_rights > num_lefts:
                tex = "{" + tex
                num_lefts += 1
            while num_lefts > num_rights:
                tex = tex + "}"
                num_rights += 1
            return tex

        #Function returning number of vertices based on the iteration number
        def GetNumberOfVertices(iteration):
            vertices = 3*4**(iteration)
            return vertices
        
        #Function returning all of the new operators based on
        #the previous iteration of operators
        def GetOperators(x_operators, y_operators, iteration):

            new_x_operators = []
            new_y_operators = []

            number_vertices = GetNumberOfVertices(iteration=iteration)

            #Formula for finding the cycle shift, with one exception on iteration 2
            if iteration == 1:
                cycle_shift = 2
            else:
                cycle_shift = 2*4**(iteration-2)

            for _ in range(6):

                #Shift the horizontal operator cycle by 2
                temp = x_operators[:cycle_shift]
                x_operators = x_operators[cycle_shift:]
                x_operators += temp

                operator_group = x_operators[:int(number_vertices / 6)]
                new_x_operators += operator_group

                #Shift the vertical operator cycle by 2
                temp = y_operators[:cycle_shift]
                y_operators = y_operators[cycle_shift:]
                y_operators += temp

                operator_group = y_operators[:int(number_vertices / 6)]
                new_y_operators += operator_group

            return new_x_operators, new_y_operators
        
        #Function returning all of the vertices based on the iteration
        def GetVertices(x_operators, y_operators, iteration):
            vertex = dl
            vertices = [vertex]

            #Get all vertices
            for i in range(GetNumberOfVertices(iteration=iteration)):

                if (i + 1) % 3 != 0:
                    vertex = [vertex[0] + (side_length/2)*x_operators[i], 
                            vertex[1] + height*y_operators[i], 
                            0]
                else:
                    vertex = [vertex[0] + (side_length)*x_operators[i], 
                            vertex[1], 
                            0]

                vertices.append(vertex)
            
            return vertices
        
        #Function for cycling the operators to the correct location
        def CycleOperators(x_operators, y_operators, iteration):
            cycle_shift = 28*4**(iteration-2)

            #Shift horizontal operators to the correct cycle
            temp = x_operators[:cycle_shift]
            x_operators = x_operators[cycle_shift:]
            x_operators += temp

            #Shift vertical operators to the correct cycle
            temp = y_operators[:cycle_shift]
            y_operators = y_operators[cycle_shift:]
            y_operators += temp

            return x_operators, y_operators
        
                
        #Assigns side length and height of the first triangle
        tri = Triangle().scale(2).shift(UP*1.5)

        dl = tri.get_corner(DL)
        dr = tri.get_corner(DR)
        u = tri.get_top()
        
        side_length = dr[0] - dl[0]
        height = u[1] - dl[1]
        center = tri.get_bottom() + [0, height/3, 0]


        #---ITERATION 0---#
        v1 = dl
        v2 = [v1[0]+side_length/2, v1[1]+height, 0]
        v3 = [v2[0]+side_length/2, v2[1]-height, 0]

        #Create drawing
        iter0 = Polygon(v1, v2, v3, 
                        fill_color=BLUE, fill_opacity=1,
                        stroke_color=WHITE)
        
        #Sets first iteration number to be 0
        n = 0

        #Label iteration
        font_size = 30
        iter0_text = Tex(f"Iteration: $n={n}$", font_size=font_size).to_edge(UP, buff=5).align_to(tri, LEFT)

        #Area text
        def GetAreaText():
            tex = MathTex(r"\text{Area: } a_{", n, r"}=", font_size=font_size).next_to(iter0_text, DOWN).align_to(iter0_text, LEFT)
            return remove_stray_braces(tex)
        iter0_area_text = GetAreaText()
        iter0_area_text_value = MathTex("1", font_size=font_size).move_to(center)
        

        self.play(Create(iter0), Write(iter0_text))
        self.play(GrowFromCenter(iter0_area_text_value), Write(iter0_area_text))

        #Move the area text in the triangle to the area text label
        self.add(iter0_area_text_value.copy())
        self.play(iter0_area_text_value.animate.next_to(iter0_area_text, buff=0.15))


        #---ITERATION 1---#
        side_length /= 3
        height /= 3

        #Pattern: --+-++++-+--
        x_pattern = [-1, -1, 1, -1, 1, 1, 1, 1, -1, 1, -1, -1]        

        #Pattern: +O++O+-O--O-
        y_pattern = [1, 0, 1, 1, 0, 1, -1, 0, -1, -1, 0, -1]

        #Get all operators
        x_operators, y_operators = GetOperators(x_operators=x_pattern, y_operators=y_pattern, iteration=1)

        #Get all vertices
        vertices = GetVertices(x_operators=x_operators, y_operators=y_operators, iteration=1)
        
        #Create drawing
        iter1 = Polygon(*vertices,
                        fill_color=BLUE, fill_opacity=1,
                        stroke_color=WHITE)
        
        #Create a copy of the previous iteration to keep triangular lines
        self.bring_to_back(iter0.copy())
        self.bring_to_back(iter0)
        

        n += 1
        #Label iteration
        iter1_text = Tex(f"Iteration: $n={n}$", font_size=font_size).to_edge(UP, buff=5).align_to(iter0_text, LEFT)
        
        #Area text
        iter1_area_text = GetAreaText()

        #Animation
        self.play(ReplacementTransform(iter0, iter1),
                  ReplacementTransform(iter0_text, iter1_text),
                  ReplacementTransform(iter0_area_text, iter1_area_text),
                  run_time=1)
        
        


        rotation = PI/6
        scale = 4/3
        one_ninths = VGroup()
        for _ in range(3):
            one_ninth = MathTex(r"\frac{1}{9}", font_size=28).move_to(center).shift(RIGHT*np.cos(rotation)*scale).shift(UP*np.sin(rotation)*scale).shift(DOWN*0.05)
            one_ninths.add(one_ninth)
            rotation += 2*PI/3
        self.play(GrowFromPoint(mobject=one_ninths.copy(), point=center))

        plus_3_times_one_ninth = MathTex("+", "3", r"(\phantom{1 \over 9})", font_size=font_size).next_to(iter0_area_text_value, buff=0.05).shift(DOWN*0.025)
        self.play(Write(plus_3_times_one_ninth))

        self.play(AnimationGroup(*[mob.animate.move_to([0.67, -1.64, 0]) for mob in one_ninths]))

        
        #---ITERATION 2---#
        side_length /= 3
        height /= 3

        #Get all the operators
        x_operators, y_operators = GetOperators(x_operators=x_operators, y_operators=y_operators, iteration=2)

        #Cycle all the operators
        x_operators, y_operators = CycleOperators(x_operators=x_operators, y_operators=y_operators, iteration=2)

        #Get all the vertices
        vertices = GetVertices(x_operators=x_operators, y_operators=y_operators, iteration=2)

        #Create drawing
        iter2 = Polygon(*vertices,
                        fill_color=BLUE, fill_opacity=1,
                        stroke_color=WHITE)
        
        #Label iteration
        n += 1
        iter2_text = Tex(f"Iteration: $n={n}$", font_size=font_size).to_edge(UP, buff=5).align_to(iter0_text, LEFT)
        

        #Create a copy of the previous iteration to keep triangular lines
        self.bring_to_back(iter1.copy())
        self.bring_to_back(iter1)
        
        #Area Text
        iter2_area_text = GetAreaText()

        #Animation
        self.play(ReplacementTransform(iter1, iter2), 
                ReplacementTransform(iter1_text, iter2_text),
                ReplacementTransform(iter1_area_text, iter2_area_text),
                run_time=1)


        #Area text
        one_ninth_squareds = VGroup()

        scale = 2.1
        rotation = 3*PI/48

        for i in range(12):
            one_ninth_squared = MathTex(r"\frac{1}{9^2}", font_size=25).move_to(center).shift(RIGHT*np.cos(rotation)*scale).shift(UP*np.sin(rotation)*scale)
            one_ninth_squareds.add(one_ninth_squared)
            if i % 2 == 0:
                rotation += 42*DEGREES
            else:
                rotation += 17*DEGREES

        self.play(GrowFromPoint(mobject=one_ninth_squareds, point=center))

        plus_12_times_one_ninth_squared = MathTex("+", "12", r"(\phantom{\frac{1}{9^2}})", font_size=font_size).next_to(plus_3_times_one_ninth, buff=0.05)
        self.play(Write(plus_12_times_one_ninth_squared))

        self.play(AnimationGroup(*[mob.animate.set(font_size=font_size).move_to([1.77, -1.64, 0]) for mob in one_ninth_squareds]))


        #---ITERATION 3---#
        side_length /= 3
        height /= 3

        #Get all the operators
        x_operators, y_operators = GetOperators(x_operators=x_operators, y_operators=y_operators, iteration=3)

        #Cycle all the operators
        x_operators, y_operators = CycleOperators(x_operators=x_operators, y_operators=y_operators, iteration=3)

        #Get all the vertices
        vertices = GetVertices(x_operators=x_operators, y_operators=y_operators, iteration=3)

        #Create drawing
        iter3 = Polygon(*vertices,
                        fill_color=BLUE, fill_opacity=1,
                        stroke_color=WHITE)
        
        #Label iteration
        n += 1
        iter3_text = Tex(f"Iteration: $n={n}$", font_size=font_size).to_edge(UP, buff=5).align_to(iter0_text, LEFT)
        

        #Create a copy of the previous iteration to keep triangular lines
        self.bring_to_back(iter2.copy())
        self.bring_to_back(iter2)
        
        #Area Text
        iter3_area_text = GetAreaText()

        #Animation
        self.play(ReplacementTransform(iter2, iter3), 
                ReplacementTransform(iter2_text, iter3_text),
                ReplacementTransform(iter2_area_text, iter3_area_text),
                run_time=1)


        #Area text
        one_ninth_cubed = r"\frac{1}{9^3}"
        plus_48_times_one_ninth_cubed = MathTex("+", "48", f"({one_ninth_cubed})", font_size=font_size).next_to(plus_3_times_one_ninth, DL, buff=0.1)
        self.play(Write(plus_48_times_one_ninth_cubed))


        #---ITERATION 4---#
        side_length /= 3
        height /= 3

        #Get all the operators
        x_operators, y_operators = GetOperators(x_operators=x_operators, y_operators=y_operators, iteration=4)

        #Cycle all the operators
        x_operators, y_operators = CycleOperators(x_operators=x_operators, y_operators=y_operators, iteration=4)

        #Get all the vertices
        vertices = GetVertices(x_operators=x_operators, y_operators=y_operators, iteration=4)

        #Create drawing
        iter4 = Polygon(*vertices,
                        fill_color=BLUE, fill_opacity=1,
                        stroke_color=WHITE)
        
        #Label iteration
        n += 1
        iter4_text = Tex(f"Iteration: $n={n}$", font_size=font_size).to_edge(UP, buff=5).align_to(iter0_text, LEFT)
        

        #Create a copy of the previous iteration to keep triangular lines
        self.bring_to_back(iter3.copy())
        self.bring_to_back(iter3)
        
        #Area Text
        iter4_area_text = GetAreaText()

        #Animation
        self.play(ReplacementTransform(iter3, iter4), 
                ReplacementTransform(iter3_text, iter4_text),
                ReplacementTransform(iter3_area_text, iter4_area_text),
                run_time=1)


        #Area text
        one_ninth_4th_power = r"\frac{1}{9^4}"
        plus_192_times_one_ninth_4th_power = MathTex("+", "192", f"({one_ninth_4th_power})", "...", font_size=font_size).next_to(plus_48_times_one_ninth_cubed, buff=0.1)
        self.play(AnimationGroup(*[Write(plus_192_times_one_ninth_4th_power[i]) for i in range(3)]))
        self.play(Write(plus_192_times_one_ninth_4th_power[3]))


        #---COEFFICIENTS---#

        coefficients = VGroup(*[mob[1].copy() for mob in [plus_3_times_one_ninth, plus_12_times_one_ninth_squared, plus_48_times_one_ninth_cubed, plus_192_times_one_ninth_4th_power]])
        area_equation = VGroup(iter0_area_text, 
                               iter1_area_text,
                               iter2_area_text,
                               iter3_area_text,
                               iter4_area_text,
                               iter0_area_text_value,
                               plus_3_times_one_ninth,
                               plus_12_times_one_ninth_squared,
                               plus_48_times_one_ninth_cubed,
                               plus_192_times_one_ninth_4th_power,
                               one_ninths,
                               one_ninth_squareds)
                                
        self.play(area_equation.animate.shift(DOWN*5),
                  coefficients.animate.arrange(buff=0.25).move_to([0, coefficients.get_y(), 0]))
        

        #Creates commas in between each coefficient
        comma = MathTex(",", font_size=font_size)
        commas = VGroup(*[comma.copy().next_to(coefficients[i], DR, buff=0.05).shift(UP*0.05) for i in range(len(coefficients)-1)])
        self.play(Write(commas))

        #Writes an equation for the number of new triangles
        T_n = MathTex("T_n = ", "3", r"\cdot", "4^{n-1}", font_size=font_size).next_to(coefficients, DOWN, buff=0.25)
        self.play(Write(T_n))
        self.wait(0.5)
        split_up = MathTex(r"\frac{4^n}{4^1}", font_size=font_size).next_to(T_n[2], buff=0.1)
        self.play(ReplacementTransform(T_n[3], split_up))
        self.wait(0.5)
        better_T_n = MathTex(r"\frac{3}{4} \cdot 4^n", font_size=font_size).next_to(T_n[0], buff=0.1)
        self.play(ReplacementTransform(T_n[1:], better_T_n))
        self.wait(0.5)

        new_area_equation = MathTex(r"\text{Area: } a_n = ", 
                                    r"1+",
                                    r"T_1(\frac{1}{9^1})+ ",
                                    r"T_2(\frac{1}{9^2})+",
                                    r"...", font_size=font_size-10).next_to(iter4_text, DOWN, buff=0.25).set_x(0).shift(DOWN*5)
        self.add(new_area_equation)
        self.play(Unwrite(VGroup(coefficients, commas)))
        self.play(new_area_equation.animate.shift(UP*5))
        self.wait(0.5)

        general_area_equation = MathTex(r"\text{Area: } a_n = ", 
                                    r"1+",
                                    r"T_1(\frac{1}{9^n})+",
                                    r"T_2(\frac{1}{9^n})+",
                                    r"...", font_size=font_size-10).match_coord(new_area_equation, dim=1)
        
        self.play(ReplacementTransform(new_area_equation, general_area_equation))
        self.wait(0.5)

        sum_equation = MathTex(r"\text{Area: } a_n = 1 +", 
                               r"\sum_{k=1}^{n}", 
                               r"T_k",
                               r"(\frac{1}{9^k})",
                               font_size=font_size-5).match_coord(general_area_equation, dim=1)
        
        self.play(ReplacementTransform(general_area_equation, sum_equation))
        self.wait(0.5)

        T_k = MathTex(r"\frac{3}{4} \cdot", r"4^k",
                              font_size=font_size-5).move_to(sum_equation[2].get_center())
        phantom_T_k = SurroundingRectangle(T_k).set_stroke(width=0)
        
        self.play(VGroup(sum_equation[:2], phantom_T_k, sum_equation[3]).animate.arrange(buff=0).match_coord(sum_equation, dim=1),
                  ReplacementTransform(sum_equation[2], T_k),
                  Unwrite(VGroup(T_n[0], better_T_n, split_up)))
        self.wait(0.5)

        shuffle = MathTex(r"\left(\frac{4^k}{9^k}\right)",
                          font_size=font_size-5).move_to(VGroup(T_k[1], sum_equation[3]).get_center()).shift(LEFT*0.1)
        
        self.play(ReplacementTransform(VGroup(T_k[1], sum_equation[3]), shuffle))
        self.wait(0.5)

        final = MathTex(r"\left(\frac{4}{9}\right)^{k}", font_size=font_size-5).move_to(shuffle.get_center())

        self.play(ReplacementTransform(shuffle, final))
        self.wait(0.5)

        
        #---ITERATION 5 AND BEYOND---#
        
        def GetAreaValue(iteration):
            addends = []
            for i in range(iteration):
                addends.append((3/4)*(4/9)**(i+1))

            return MathTex(round(sum(addends, 1), 5), font_size=font_size)

        #Label iteration
        old_iter_text = iter4_text
        old_area_text = iter4_area_text
        old_area_text_value = iter0_area_text_value
        for i in range(11):
            n += 1
            new_iter_text = Tex(f"Iteration: $n={n}$", font_size=font_size).to_edge(UP, buff=5).align_to(iter0_text, LEFT)

            #Area Text
            new_area_text = GetAreaText().next_to(iter0_text, DOWN, buff=0.9)
            new_area_text_value = GetAreaValue(n).next_to(new_area_text, buff=0.15)

            #Animation
            self.play(ReplacementTransform(old_iter_text, new_iter_text),
                      ReplacementTransform(old_area_text, new_area_text),
                      ReplacementTransform(old_area_text_value, new_area_text_value),
                      run_time=0.5)
             
            old_iter_text = new_iter_text
            old_area_text = new_area_text
            old_area_text_value = new_area_text_value

        self.wait(0.5)
        n_to_infinity = MathTex(r"\text{Area:} \lim_{n \to \infty} a_n =", r"1.6", font_size=font_size).match_y(old_area_text).shift(DOWN*0.25).align_to(old_area_text, LEFT)
        self.play(ReplacementTransform(VGroup(old_area_text, old_area_text_value), n_to_infinity))
        self.wait(0.5)

        eight_fifths = MathTex(r"\frac{8}{5}", font_size=font_size).next_to(n_to_infinity[0], buff=0.1)
        self.play(ReplacementTransform(n_to_infinity[1], eight_fifths))

        self.play(Circumscribe(eight_fifths))
        
        

        self.wait(2)