import re
from textprocess import change_sigla

def tex_output(filename):
    chapter = 0
    vsnum = 0
    onflag = False
    textflag = False
    appflag = False
    paralflag = False
    anustubh = True
    hemistich = 0
    proseflag = False
    pvarflag = False
    just_uvaca = False
    print("\\renewcommand{\\dnapp}[1]{}\\renewcommand{\\rmapp}[1]{#1}")
    print("\\fejno=0\\versno=0")
    openfile = open(filename, "r")
    for line in openfile:
        if '<START/>' in line:
            onflag = True
        if '<STOP/>' in line:
            onflag = False
        if '<NOTANUSTUBH/>' in line:
            #print("\n\\nemsloka ")
            anustubh = False 
            proseflag = False
            hemistich = 0
        if '<ANUSTUBH/>' in line:
            print("\n\\vers")
            anustubh = True
            proseflag = False
            #hemistich = 0
        if '<LONGVERSELINES/>' in line:
            print("\n\\nemslokalong\n")
        if '<NORMALVERSELINES/>' in line:
            print("\n\\nemslokanormal\n")
        if '<LITEM/>' in line:
            print("\n")
        if '<PROSE>' in line and onflag == True:
            proseflag = True
            anustubh = False
            print("\n\\prose%")
        if '</PROSE>' in line:
            proseflag = False
        if '<SETVSNUM' in line:
            v01 = re.sub('.*<SETVSNUM="', '', line)
            v01 = re.sub('".*', '', v01)
            vsnum = int(v01) - 1
            print("\\versno=" + str(vsnum))
        if '<NEWCHAPTER/>' in line and onflag == True:
            if chapter > 0:
                #print("\\bekveg\\szamveg\\vfill\\phpspagebreak\\ujfej\\szam\\bek\n")
                v01 = "\nBACKSLASHugrasBACKSLASHujfej"
            else:
                v01 = "BACKSLASHujfejBACKSLASHszamBACKSLASHbek\n"
            v01 = re.sub('BACKSLASH', '\\\\', v01)
            print(v01)
            chapter += 1
            vsnum = 0
            hemistich = 0
        # if it is the main text:        
        if ('<TEXT>' in line or textflag == True) and onflag == True:
            textflag = True
            if '</TEXT>' in line:
                textflag = False
            # check if this is the end of a verse
            if '||' in line and anustubh == True and proseflag == False:
                outputline = re.sub('\|\|', ' \\\\vegBACKSLASHdontdisplaylinenum', line)
                hemistich = 0
            elif '||' in line and anustubh == False and proseflag == False:
                outputline = re.sub('\|\|', ' \\\\vegBACKSLASHdontdisplaylinenum', line)
                outputline = "\n\\nemslokad " + outputline 
                hemistich = 0
            elif '||' in line and anustubh == False and proseflag == True:
                outputline = re.sub('\|\|', '\\\\thinspace{\\\\ketdanda}', line)
            elif '|' in line and anustubh == False and proseflag == True:
                outputline = re.sub('\|', '\\\\thinspace{\\\\danda}', line)
            # special danda: it does increase verse number, e.g. after devy uvāca, but sets the next dandab to danda
            elif '|*' in line and proseflag == False:
                outputline = re.sub('\|\*', '~{\\\\dandab}BACKSLASHdontdisplaylinenum ', line)
                just_uvaca = True
            # with anuṣṭubh, a danda increases verse number if it is the first single danda
            elif '|' in line and hemistich == 0 and anustubh == True and proseflag == False:
                if just_uvaca == False:
                    outputline = re.sub('\|', '\\\\thinspace{\\\\dandab} BACKSLASHdontdisplaylinenum', line)
                else:
                    outputline = re.sub('\|', '\\\\thinspace{\\\\danda} BACKSLASHdontdisplaylinenum', line)
                    # the next single danda not a first single danda
                hemistich = 1 
                just_uvaca = False
            # if this is a first single danda but it is not anuṣṭubh, don't increase verse number    
            elif '|' in line and anustubh == False and proseflag == False:
                outputline = re.sub('\|', ' \\\\dandaBACKSLASHdontdisplaylinenum', line)
                outputline = "\n\\nemslokab " + outputline
                hemistich = hemistich + 1 
            elif '|' in line and hemistich > 0 and anustubh == True and proseflag == False:
                outputline = re.sub('\|', ' \\\\dandaBACKSLASHdontdisplaylinenum', line)
                hemistich = hemistich + 1 
            # check if this is a non-anuṣṭubh first line
            elif '|' not in line and hemistich == 0 and anustubh == False and proseflag == False:
                if just_uvaca == False:
                    # no indent
                    outputline = "\nBACKSLASHujversBACKSLASHnemsloka " + line + "BACKSLASHdontdisplaylinenum "
                else:
                    outputline = "\nBACKSLASHnemsloka " + line + "BACKSLASHdontdisplaylinenum "
                hemistich = 1
                just_uvaca = False
            elif '|' not in line and hemistich == 2 and anustubh == False and proseflag == False:
                # no indent
                outputline = "\nBACKSLASHnemslokac " + line + "BACKSLASHdontdisplaylinenum "
                hemistich = hemistich + 1
            else:
                outputline = line
            # simple substitutions
            if proseflag == False:
                v01 = re.sub('<TEXT> ?', '\n', outputline[:-1])
            if proseflag == True:
                v01 = re.sub('<TEXT> ?', '', outputline[:-1])
            # to eliminate spaces in prose passages    
            if proseflag == False:
                v01 = re.sub('</TEXT>.*', '', v01)
            else:
                v01 = re.sub('</TEXT>.*', '%', v01)
            v01 = re.sub('</PROSE>', '', v01)
            v01 = re.sub('<PROSE> ?', '', v01)
            v01 = re.sub('<MNTR>', '\\\\mntr{', v01)
            v01 = re.sub('</MNTR>', '}', v01)
            v01 = re.sub('<LITEM/>', '', v01)
            v01 = re.sub('{ }', " ", v01)
            v01 = re.sub('<COLOPHON>', "\n\\\\ugras\n\\\\begin{center}\nBACKSLASHketdanda ", v01)
            v01 = re.sub('</COLOPHON>', "BACKSLASHketdanda\n\\\\end{center}\n\\\\dontdisplaylinenum\\\\vers ", v01)
            v01 = re.sub('Ó', '{\\\\dn :}', v01)
            v01 = re.sub('ṝ', '\\\d{\\\=r}', v01)
            v01 = re.sub('ḹ', '\\\d{\\\=l}', v01)
            v01 = re.sub('<uvaca>', '', v01)
            v01 = re.sub('</uvaca>', '', v01)
            v01 = re.sub('\*', '{\il}', v01)
            v01 = re.sub('×', '{\lost}', v01)
            v01 = re.sub('<ja>', ' ', v01)
            v01 = re.sub('</ja>', ' ', v01)
            v01 = re.sub('BACKSLASH', '\\\\', v01)
            print(v01)
        if ('<APP>' in line or appflag == True) and onflag == True:
            appflag = True
            v01 = re.sub('<APP> ?', '    \\\\var{', line[:-1])
            if '</APP>' in line:
                appflag = False
            v01 = re.sub(' ?</APP>', '}%', v01)
            v01 = re.sub('{ }', " ", v01)
            v01 = re.sub('<LEM>', '', v01)
            v01 = re.sub('</LEM>', '\lem ', v01)
            v01 = re.sub('<UNCL>', '\\\\uncl{', v01)
            v01 = re.sub('</UNCL>', '}', v01)
            v01 = re.sub('<MNTR>', '\\\\mntr{', v01)
            v01 = re.sub('</MNTR>', '}', v01)
            v01 = re.sub('<EYESKIPTO>', '\\\\eyeskipto{', v01)
            v01 = re.sub('</EYESKIPTO>', '}', v01)
            v01 = re.sub('ṝ', '\\\d{\\\=r}', v01)
            v01 = re.sub('ḹ', '\\\d{\\\=l}', v01)
            v01 = re.sub('\\Ł', '{\\\\normalfont ', v01)
            v01 = re.sub('\\$', '}', v01)
            v01 = re.sub('\\\\csa', '{ā}', v01)
            v01 = re.sub('\\\\csi', '{i}', v01)
            v01 = re.sub('\|', '{\\\\danda}', v01)
            v01 = change_sigla.change_sigla(v01)
            print(v01)
        if ('<PARAL>' in line or paralflag == True) and onflag == True:
            paralflag = True
            if '</PARAL>' in line:
                paralflag = False
            v01 = re.sub('{ }', " ", line)
            v01 = re.sub('<PARAL>', '    \\\\paral{\\\\textit{', v01[:-1])
            v01 = re.sub('</PARAL>', '}}', v01)
            v01 = re.sub('{ }', " ", v01)
            v01 = re.sub('\\Ł', '{\\\\normalfont ', v01)
            v01 = re.sub('\\$', '}', v01)
            v01 = re.sub('\|\|', '{\\\\thinspace\ketdanda}', v01)
            v01 = re.sub('\|', '{\\\\thinspace\danda}', v01)
            print(v01)
        if ('<PVAR>' in line or pvarflag == True) and onflag == True:
            pvarflag = True
            if '</PVAR>' in line:
                pvarflag = False
            v01 = re.sub('{ }', " ", line)
            v01 = re.sub('<PVAR>', '    \\\\prosevar{', v01[:-1])
            v01 = re.sub('</PVAR>', '}%', v01)
            v01 = re.sub('<LEM>', '', v01)
            v01 = re.sub('</LEM>', '\lem ', v01)
            v01 = re.sub('\\Ł', '\\\\skt{', v01)
            v01 = re.sub('\\$', '}', v01)
            print(v01)
        if '<SUBCHAPTER>' in line and onflag == True:
            v01 = re.sub('<SUBCHAPTER>', '\n\n\\\\alalfejezet{', line[:-1])
            v01 = re.sub('</SUBCHAPTER>', '}', v01)
            v01 = re.sub('{ }', " ", v01)
            print(v01, end="")
        if '<CHAPTER>' in line and onflag == True:
            v01 = re.sub('<CHAPTER>', '\n\n\\\\alfejezet{\\\\textbf{', line[:-1])
            v01 = re.sub('</CHAPTER>', '}}', v01)
            v01 = re.sub('{ }', " ", v01)
            print(v01, end="")
        if '<TITLE>' in line and onflag == True:
            v01 = re.sub('<TITLE>', '\\\\begin{center}{\Huge  ', line[:-1])
            v01 = re.sub('</TITLE>', '}\\\\end{center}', v01)
            v01 = re.sub('{ }', "", v01)
            print(v01, end="")
        if '<TAMIL>' in line and onflag == True:
            v01 = re.sub('<TAMIL>', '', line[:-1])
            v01 = re.sub('</TAMIL>', '', v01)
            #v01 = tamil.txt2unicode.diacritic2unicode(v01)
            print(v01, "\n")
    openfile.close()


