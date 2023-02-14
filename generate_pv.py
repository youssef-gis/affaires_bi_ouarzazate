from fpdf import FPDF





def generate_pv(EXERCICE_BUDGETAIRE_YEAR, NATURE_DU_DOSSIER, NUMERO_PV, Date_du_PV, Date_du_PV_month,  affaires_livree, Retard_Livree, Retard_Rejetee,nbr_affaires_non_acceptes,
                        nbr_affaires_non_Livrees, nbr_affaires_non_recuperees, nbr_affaires_retournee_sans_levee, filtered_df  ):
    title_0 = "ROYAUME DU MAROC"
    title_1 ="AGENCE NATIONALE DE LA CONSERVATION FONCIERE DU CADASTRE ET DE LA CARTOGRAPHIE"
    title_2 ="DIRECTION DU CADASTRE"
    title_3 ="SERVICE DU CADASTRE D' OUARZAZATE"
    title_4 = "EXERCICE BUDGETAIRE :"+ str(EXERCICE_BUDGETAIRE_YEAR) +"\n NATURE DU DOSSIER :"+ NATURE_DU_DOSSIER
    title_5 = "PROCES-VERBAL DE RECEPTION PROVISOIRE N°"+ str(NUMERO_PV) +" ET DERNIER DE L'EXERCICE "+str(EXERCICE_BUDGETAIRE_YEAR)
    title_6 = "PV de la commande du Mois de : "+str(Date_du_PV_month)

    french_months = {1: "Janvier", 2: "Février", 3: "Mars", 4: "Avril", 5: "Mai", 6: "Juin",
                  7: "Juillet", 8: "Août", 9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Décembre"}

    month_name = french_months[Date_du_PV_month]
    class PDF(FPDF):
        def big_title(self):

            self.set_font('helvetica', 'BU', 10)
            
            title_w_0 = self.get_string_width(title_0) + 6
            title_w_1 = self.get_string_width(title_1) + 6
            doc_w= self.w

            self.set_x((doc_w - title_w_0)/2)
            
            self.set_draw_color(0, 0, 0)

            self.set_fill_color(225, 225, 225)

            self.set_text_color(0, 0, 0)
            self.set_line_width(1)
    
            self.cell(title_w_0, 5, title_0, border=False, ln=1, align='C', fill=False)
            self.cell(190, 5, title_1, border=False, ln=1, align='C', fill=False)
            self.cell(190, 5, title_2, border=False, ln=1, align='C', fill=False)
            self.cell(190, 5, title_3, border=False, ln=1, align='C', fill=False)
            
            self.ln(5)

            self.multi_cell(190, 5, title_4, border=True, align='C', fill=False)

            self.ln(2)

            self.cell(190, 5, title_5, border=False, ln=1, align='C', fill=False)

            self.ln(6)

            self.cell(190, 5, title_6, border=False, ln=1, align='C', fill=False)


        def footer(self) -> None:
            self.set_y(-15)
            self.set_font('helvetica', 'I', 10)
            self.set_text_color(169, 169, 169)
            self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

        def chapter_title(self, ch_title):

            self.set_font('helvetica', 'B',12)
        
            self.set_fill_color(225, 225, 225)

            self.cell(0, 5, ch_title, ln=1, fill=True , align='C', border=True)

            

        def chapter_body(self, name):

            with open(name, 'rb') as fh:
                txt = fh.read().decode('UTF-8')

            self.set_font('times', '', 12)

            self.multi_cell(0, 5, txt, border=True, align='C')

            self.ln()
        
        def sub_title(self, subtitle):
            self.set_font('times', 'B', 12)

            self.cell(0, 5, subtitle)

            self.ln()
        
        def print_chapter(self, ch_title, name):
            self.chapter_title(ch_title)
            self.chapter_body(name)

        #####################################
        def create_pdf_table(self,table_data, title='', data_size = 10, title_size=12, align_data='L', align_header='L', cell_width='even', x_start='x_default',
                        emphasize_data=[], emphasize_style=None, emphasize_color=(0,0,0)):
            """
            table_data: 
                        list of lists with first element being list of headers
            title: 
                        (Optional) title of table (optional)
            data_size: 
                        the font size of table data
            title_size: 
                        the font size fo the title of the table
            align_data: 
                        align table data
                        L = left align
                        C = center align
                        R = right align
            align_header: 
                        align table data
                        L = left align
                        C = center align
                        R = right align
            cell_width: 
                        even: evenly distribute cell/column width
                        uneven: base cell size on lenght of cell/column items
                        int: int value for width of each cell/column
                        list of ints: list equal to number of columns with the widht of each cell / column
            x_start: 
                        where the left edge of table should start
            emphasize_data:  
                        which data elements are to be emphasized - pass as list 
                        emphasize_style: the font style you want emphaized data to take
                        emphasize_color: emphasize color (if other than black) 
            
            """
            default_style = self.font_style
            if emphasize_style == None:
                emphasize_style = default_style
            # default_font = pdf.font_family
            # default_size = pdf.font_size_pt
            # default_style = pdf.font_style
            # default_color = pdf.color # This does not work

            # Get Width of Columns
            def get_col_widths():
                col_width = cell_width
                if col_width == 'even':
                    col_width = self.epw / len(data[0]) - 1  # distribute content evenly   # epw = effective page width (width of page not including margins)
                elif col_width == 'uneven':
                    col_widths = []

                    # searching through columns for largest sized cell (not rows but cols)
                    for col in range(len(table_data[0])): # for every row
                        longest = 0 
                        for row in range(len(table_data)):
                            cell_value = str(table_data[row][col])
                            value_length = self.get_string_width(cell_value)
                            if value_length > longest:
                                longest = value_length
                        col_widths.append(longest + 4) # add 4 for padding
                    col_width = col_widths



                            ### compare columns 

                elif isinstance(cell_width, list):
                    col_width = cell_width  # TODO: convert all items in list to int        
                else:
                    # TODO: Add try catch
                    col_width = int(col_width)
                return col_width

            # Convert dict to lol
            # Why? because i built it with lol first and added dict func after
            # Is there performance differences?
            if isinstance(table_data, dict):
                header = [key for key in table_data]
                data = []
                for key in table_data:
                    value = table_data[key]
                    data.append(value)
                # need to zip so data is in correct format (first, second, third --> not first, first, first)
                data = [list(a) for a in zip(*data)]

            else:
                header = table_data[0]
                data = table_data[1:]

            line_height = self.font_size * 2.5

            col_width = get_col_widths()
            self.set_font(size=title_size)

            # Get starting position of x
            # Determin width of table to get x starting point for centred table
            if x_start == 'C':
                table_width = 0
                if isinstance(col_width, list):
                    for width in col_width:
                        table_width += width
                else: # need to multiply cell width by number of cells to get table width 
                    table_width = col_width * len(table_data[0])
                # Get x start by subtracting table width from pdf width and divide by 2 (margins)
                margin_width = self.w - table_width
                # TODO: Check if table_width is larger than pdf width

                center_table = margin_width / 2 # only want width of left margin not both
                x_start = center_table
                self.set_x(x_start)
            elif isinstance(x_start, int):
                self.set_x(x_start)
            elif x_start == 'x_default':
                x_start = self.set_x(self.l_margin)


            # TABLE CREATION #

            # add title
            if title != '':
                self.multi_cell(0, line_height, title, border=0, align='j', ln=3, max_line_height=self.font_size)
                self.ln(line_height) # move cursor back to the left margin

            self.set_font(size=data_size)
            # add header
            y1 = self.get_y()
            if x_start:
                x_left = x_start
            else:
                x_left = self.get_x()
            x_right = pdf.epw + float(x_left )
            if  not isinstance(col_width, list):
                if x_start:
                    self.set_x(float(x_start))
                for datum in header:
                    self.multi_cell(col_width, line_height, datum, border=0, align=align_header, ln=3, max_line_height=self.font_size)
                    x_right = self.get_x()
                self.ln(line_height) # move cursor back to the left margin
                y2 = pdf.get_y()
                self.line(float(x_left),y1,x_right,y1)
                self.line(float(x_left),y2,x_right,y2)

                for row in data:
                    if x_start: # not sure if I need this
                        self.set_x(int(x_start))
                    for datum in row:
                        if datum in emphasize_data:
                            self.set_text_color(*emphasize_color)
                            self.set_font(style=emphasize_style)
                            self.multi_cell(col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=self.font_size)
                            self.set_text_color(0,0,0)
                            self.set_font(style=default_style)
                        else:
                            self.multi_cell(col_width, line_height, datum, border=False, align=align_data, ln=3, max_line_height=self.font_size) # ln = 3 - move cursor to right with same vertical offset # this uses an object named pdf
                    self.ln(line_height) # move cursor back to the left margin
            
            else:
                if x_start:
                    self.set_x(int(x_start))
                for i in range(len(header)):
                    datum = header[i]
                    self.multi_cell(col_width[i], line_height, datum, border=0, align=align_header, ln=3, max_line_height=self.font_size)
                    x_right = self.get_x()
                self.ln(line_height) # move cursor back to the left margin
                y2 = self.get_y()
                self.line(float(x_left),y1,float(x_right),y1)
                self.line(float(x_left),y2,float(x_right),y2)


                for i in range(len(data)):
                    if x_start:
                        self.set_x(int(x_start))
                    row = data[i]
                    for i in range(len(row)):
                        datum = row[i]
                        if not isinstance(datum, str):
                            datum = str(datum)
                        adjusted_col_width = col_width[i]
                        if datum in emphasize_data:
                            self.set_text_color(*emphasize_color)
                            self.set_font(style=emphasize_style)
                            self.multi_cell(adjusted_col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=self.font_size)
                            self.set_text_color(0,0,0)
                            self.set_font(style=default_style)# type: ignore                
                        else:
                            self.multi_cell(adjusted_col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=self.font_size) # ln = 3 - move cursor to right with same vertical offset # this uses an object named pdf
                    self.ln(line_height) # move cursor back to the left margin
            y3 = self.get_y()
            self.line(float(x_left),y3,x_right,y3)
        #########################################

        


    pdf = PDF('P', 'mm', 'Letter')

  

    pdf.add_page()
    pdf.big_title()
    pdf.print_chapter('REFERENCES DU MARCHE', 'ch_1.txt' )
    pdf.print_chapter('OBJET DU MARCHE', 'ch_2.txt' )
    pdf.print_chapter('TITULAIRE DU MARCHE', 'ch_3.txt' )

    pdf.multi_cell(0, 5, """La commission dont les membres soussignés,s'est réunie le premier  """+  month_name+ """ pour procéder à la réception provisoire n°"""
    +str(NUMERO_PV)+""" des prestations topographiques ;\n concernant la livraison de """+str(affaires_livree)+ """ affaires ; objet du marché cité en référence.
    Conformément aux prescriptions du marché, au bordereau des prix et au détail estimatif.
    -  Ordre de service n°1 prescrivant le début d'exécution des prestations : 03/10/2022 
    - Nombre d'affaires minimum à livrer par mois (Article 21.1.3 du marché) : 80 affaires.
    """, border=0, align='C')
    pdf.ln()

    pdf.sub_title("Les retards (en jours) :")
    pdf.set_font('times','',12)
    pdf.multi_cell(0, 5,"1.Retard par rapport à la livraison : "+Retard_Livree+"\n2.Retard par rapport au rejet : "+Retard_Rejetee)


    # Add Page
    pdf.add_page()

    pdf.sub_title("Les affaires qui ne seront pas payées : ")


    pdf.set_font('times','',12)

    pdf.multi_cell(0, 5,"""1.Nombre d'affaires non acceptées suite au rejet : """+nbr_affaires_non_acceptes+"""
2.Nombre d'affaires non livrées après 60 jours suite au rejet : """+nbr_affaires_non_Livrees+"""
3.Nombre d'affaires non récupérées suite au rejet après 60 jours : """+nbr_affaires_non_recuperees+"""
4.Nombre d'affaires retournées sans levé pour cas de forces majeures : """+str(nbr_affaires_retournee_sans_levee)+"""
    """ )

    pdf.ln()
    pdf.multi_cell(0, 5, "En conséquence, nous déclarons qu'il y a lieu d'accorder la réception provisoire n°"+str(NUMERO_PV)+" de "+str(affaires_livree)+" affaires acceptées, et dans les conditions sus indiquées, le jour, mois et an ci-dessus mentionnés.")

    pdf.ln()



    pdf.sub_title("LES MEMBRES DE LA COMMISSION :")

    pdf.ln()

    pdf.set_font('times','',12)

    pdf.cell(0, 5,"Le Chef de Service :  ",ln=1)

    pdf.ln()

    pdf.cell(0, 5,"Le Chef de bureau d'immatriculation foncière :  ",ln=1)

    pdf.ln()

    pdf.cell(0, 5,"Chef du bureau de contrôle et du repérage :  ",ln=1)

    pdf.ln()

    pdf.create_pdf_table(table_data = filtered_df,title='BL du Mois de :' +  month_name, cell_width='even')
    pdf.output('pdf_1.pdf')