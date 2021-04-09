from __future__ import print_function as tk5J498S
import code as N443Zqq
import functools as Y2_5rC
import inspect as M_3u2iF
import re as wk7P0Iz0_
import signal as L6t_
import sys as L5948Fbo
import math as y4C7
import sys as L5948Fbo
import numbers as c6bb_tj_
import builtins as enIzy308_
import math as y4C7
import numbers as c6bb_tj_
import operator as V72R6_47
import sys as L5948Fbo
import builtins as enIzy308_
import itertools as n6f6_r8b_
import string as string
import sys as L5948Fbo
import tokenize as L9a3_E
import sys as L5948Fbo
import os as ml4_86Q72
import builtins as enIzy308_
'fK17Cbio9_9EM_6_E9_281_47_'

def Ad4g(r2__13):
    'a6iWT1OhEQ3Jz02P01445_'
    if M_3u2iF.stack()[(((103 + -75) + (-78 + -15)) + ((89 + 9) + (-31 + -1)))][int((((-0.9395069537591247 + 0.8847803151571815) + (0.5147059582462504 + 0.012010931498991018)) * 0))].f_locals[(('_' + ('' + '_name')) + ('_' + chr(95)))] == ((('_' + '_m') + ('' + 'ain_')) + chr((174 + -79))):
        EB1Tdm75 = L5948Fbo.argv[(((-146 + 100) + (90 + -82)) + ((119 + -45) + (56 + -91))):]
        r2__13(*EB1Tdm75)
    return r2__13
Q5463 = str()

def o4O_J(r2__13):
    'o1_5Q41_CA_a5__nBd6R'

    @Y2_5rC.wraps(r2__13)
    def g2283Q6(*EB1Tdm75, **o_1vee):
        global Q5463
        t_4R8gz = [repr(K_2f5Wj__) for K_2f5Wj__ in EB1Tdm75]
        t_4R8gz += [((repr(f_5K08) + '=') + repr(q5Y3900g)) for (f_5K08, q5Y3900g) in o_1vee.items()]
        Qy7tpB4Y((('' + (('' + '{0}(') + ('{1' + '})'))).format(r2__13.__name__, (str() + (str() + ('' + ', '))).join(t_4R8gz)) + chr(((102 + -10) + (17 + -51)))))
        Q5463 += ('' + (('' + '  ') + ('' + '  ')))
        try:
            bq9X9 = r2__13(*EB1Tdm75, **o_1vee)
            Q5463 = Q5463[:(- (((6 + -65) + (149 + -49)) + ((-19 + -53) + (56 + -21))))]
        except Exception as K_2f5Wj__:
            Qy7tpB4Y((r2__13.__name__ + (' ' + (('exite' + 'd') + (' via exce' + 'ption')))))
            Q5463 = Q5463[:(- (((100 + -39) + (-31 + -23)) + ((50 + -47) + (-8 + 2))))]
            raise
        Qy7tpB4Y((chr((143 + -20)) + (chr(48) + ('}({1}) ->' + ' {2}'))).format(r2__13.__name__, (chr((72 + -28)) + chr(32)).join(t_4R8gz), bq9X9))
        return bq9X9
    return g2283Q6

def Qy7tpB4Y(YIZ6m1):
    'd_Ej4h_6_8yD8610o714_0ve'
    print((Q5463 + wk7P0Iz0_.sub('\n', (chr((-36 + 46)) + Q5463), str(YIZ6m1))))

def D01z4XbNy():
    'c1634F7omEu594Y3SMNFE'
    henX44 = M_3u2iF.stack()[(((2 + 53) + (125 + -81)) + ((8 + -89) + (-60 + 43)))]
    Qy7tpB4Y(((('Current l' + 'i') + ('ne: ' + 'Fil')) + (('e ' + '"') + ('{f[1]}", line {f[2]' + '}, in {f[3]}'))).format(f=henX44))

def uXJES3a4M(K01443=None):
    'K_646Dq10H_c__z9lYO6x3O_K_2IG'
    henX44 = M_3u2iF.currentframe().f_back
    X2O1yr_47 = henX44.f_globals.copy()
    X2O1yr_47.update(henX44.f_locals)

    def Y8rn45(signum, henX44):
        print()
        exit(int((((-0.35919713092984773 + 0.05885323088065508) + (-0.3505569519557479 + 0.9392233376921446)) * int(((-0.10791696545751261 + 0.5201756087181908) * int((0.45397261684352086 * 0)))))))
    L6t_.signal(L6t_.SIGINT, Y8rn45)
    if (not K01443):
        (x_x07, Y27vn5, x_77522, x_x07, x_x07, x_x07) = M_3u2iF.stack()[(((151 + -33) + (-57 + -8)) + ((-2 + -5) + (-44 + -1)))]
        K01443 = ((('Interac' + 't') + ('i' + 'ng')) + ((' at Fil' + 'e "{0}') + ('", line {1' + '} \n'))).format(Y27vn5, x_77522)
        K01443 += (((' ' + '   Unix:    <Control>-D continues') + (' the p' + 'rogr')) + (('am' + ';') + ('' + ' \n')))
        K01443 += ((('    W' + 'indows: <Cont') + chr(114)) + (('ol>-Z ' + '<Enter> continues ') + ('the program; ' + '\n')))
        K01443 += ((str() + (' ' + ' ')) + ((' ' + ' exit() or <Cont') + ('rol>-C exits' + ' the program')))
    N443Zqq.interact(K01443, None, X2O1yr_47)
'tY8m_5_S2_Wf9F1_z8__Y_4'
if (L5948Fbo.version_info[0] < (((-45 + 39) + (15 + 56)) + ((-190 + 56) + (153 + -81)))):

    def input(W276Q_):
        L5948Fbo.stderr.write(W276Q_)
        L5948Fbo.stderr.flush()
        x_77522 = L5948Fbo.stdin.readline()
        if (not x_77522):
            raise EOFError()
        return x_77522.rstrip((chr((-32 + 45)) + '\n'))

class e50_T_22(object):
    'HQ885Pnl2B8A6e11A4yw8YwtW_'

    def __init__(H_9G4L_X, r_3_Ai_30):
        H_9G4L_X.index = int((0.407023944450292 * 0))
        H_9G4L_X.C3m_ = []
        H_9G4L_X.r_3_Ai_30 = r_3_Ai_30
        H_9G4L_X.current_line = ()
        H_9G4L_X.current()

    def Xz9_yJj_(H_9G4L_X):
        'v635_83_74PY1_9jmU_4xxY'
        current = H_9G4L_X.current()
        H_9G4L_X.index += (((-40 + 61) + (-38 + 96)) + ((-186 + 45) + (-1 + 64)))
        return current

    def current(H_9G4L_X):
        'kF__c_Dkb_i__3v_byTw6'
        while (not H_9G4L_X.WN0Y_):
            H_9G4L_X.index = int((0.8732780338001057 * 0))
            try:
                H_9G4L_X.current_line = next(H_9G4L_X.r_3_Ai_30)
                H_9G4L_X.C3m_.append(H_9G4L_X.current_line)
            except StopIteration:
                H_9G4L_X.current_line = ()
                return None
        return H_9G4L_X.current_line[H_9G4L_X.index]

    @property
    def WN0Y_(H_9G4L_X):
        return (H_9G4L_X.index < len(H_9G4L_X.current_line))

    def __str__(H_9G4L_X):
        'hP5YR_1Bpz54z2__x5aL526'
        e___6V_ = len(H_9G4L_X.C3m_)
        K01443 = ((((('{' + '0') + chr(58)) + chr(62)) + str((y4C7.floor(y4C7.log10(e___6V_)) + (((-5 + 25) + (-102 + 14)) + ((114 + -12) + (-118 + 85)))))) + (chr((25 + 100)) + (chr(58) + chr(32))))
        P_7q887A_ = ''
        for VE28Mj in range(max(int(((-0.6290502958546599 + 0.6737984398043014) * int((0.3230208641165697 * 0)))), (e___6V_ - (((-41 + 94) + (6 + -53)) + ((-31 + 46) + (-38 + 21))))), (e___6V_ - (((73 + -78) + (14 + -58)) + ((5 + -36) + (79 + 2))))):
            P_7q887A_ += ((K01443.format((VE28Mj + (((-116 + 23) + (-69 + 91)) + ((69 + -45) + (-29 + 77))))) + chr((-60 + 92)).join(map(str, H_9G4L_X.C3m_[VE28Mj]))) + chr((-61 + 71)))
        P_7q887A_ += K01443.format(e___6V_)
        P_7q887A_ += chr(32).join(map(str, H_9G4L_X.current_line[:H_9G4L_X.index]))
        P_7q887A_ += (str() + ((' ' + '>') + ('' + '> ')))
        P_7q887A_ += chr((88 + -56)).join(map(str, H_9G4L_X.current_line[H_9G4L_X.index:]))
        return P_7q887A_.strip()
try:
    import readline as rsvx9R
except:
    pass

class Pt06(object):
    'G43_T1S5D_4_ZQ7h6pB1__j_15_g'

    def __init__(H_9G4L_X, W276Q_):
        H_9G4L_X.W276Q_ = W276Q_

    def __iter__(H_9G4L_X):
        while True:
            (yield input(H_9G4L_X.W276Q_))
            H_9G4L_X.W276Q_ = (chr(((2 + 40) + (-75 + 65))) * len(H_9G4L_X.W276Q_))

class wV33MCA_Y(object):
    'Ey58POD6_2T1ow6__3_1B64_v'

    def __init__(H_9G4L_X, C3m_, W276Q_, J_H__h0=';'):
        H_9G4L_X.C3m_ = C3m_
        H_9G4L_X.W276Q_ = W276Q_
        H_9G4L_X.J_H__h0 = J_H__h0

    def __iter__(H_9G4L_X):
        while H_9G4L_X.C3m_:
            x_77522 = H_9G4L_X.C3m_.pop(int((0.03861882199957112 * 0))).strip(chr(((14 + -65) + (144 + -83))))
            if ((H_9G4L_X.W276Q_ is not None) and (x_77522 != str()) and (not x_77522.lstrip().startswith(H_9G4L_X.J_H__h0))):
                print((H_9G4L_X.W276Q_ + x_77522))
                H_9G4L_X.W276Q_ = (chr((-64 + 96)) * len(H_9G4L_X.W276Q_))
            (yield x_77522)
        raise EOFError
'i_9G_9C6rS_12FH39oto800H57v'
enIzy308_.DOTS_ARE_CONS = False
enIzy308_.TK_TURTLE = False
enIzy308_.TURTLE_SAVE_PATH = None

class Pair(object):
    'x3Xhf1P_665_zu5u0SA98'

    def __init__(H_9G4L_X, Wai2, H7dNr_):
        if ((not enIzy308_.DOTS_ARE_CONS) and (not M5_8uB(H7dNr_))):
            print(H7dNr_, type(H7dNr_).__name__)
            raise s600(((('cd' + 'r') + (' ' + 'c')) + (('an only be ' + 'a pa') + ('' + 'ir, nil, or a promise but was {}'))).format(H7dNr_))
        H_9G4L_X.Wai2 = Wai2
        H_9G4L_X.H7dNr_ = H7dNr_

    def __repr__(H_9G4L_X):
        return (('P' + 'a') + (str() + ('ir({0}, {1}' + ')'))).format(repr(H_9G4L_X.Wai2), repr(H_9G4L_X.H7dNr_))

    def __str__(H_9G4L_X):
        P_7q887A_ = (chr(40) + repl_str(H_9G4L_X.Wai2))
        H7dNr_ = H_9G4L_X.H7dNr_
        while isinstance(H7dNr_, Pair):
            P_7q887A_ += (chr(((60 + 48) + (-142 + 66))) + repl_str(H7dNr_.Wai2))
            H7dNr_ = H7dNr_.H7dNr_
        if (H7dNr_ is not nil):
            P_7q887A_ += ((str() + (str() + (' ' + '. '))) + repl_str(H7dNr_))
        return (P_7q887A_ + chr(((132 + -78) + (-34 + 21))))

    def __len__(H_9G4L_X):
        (e___6V_, H7dNr_) = ((((59 + 24) + (23 + -73)) + ((-49 + -38) + (-10 + 65))), H_9G4L_X.H7dNr_)
        while isinstance(H7dNr_, Pair):
            e___6V_ += (((-57 + 41) + (-169 + 90)) + ((178 + -49) + (-55 + 22)))
            H7dNr_ = H7dNr_.H7dNr_
        if (H7dNr_ is not nil):
            raise TypeError(((('length attempted on ' + 'im') + ('proper l' + 'is')) + chr((55 + 61))))
        return e___6V_

    def __eq__(H_9G4L_X, F5HAi_Iv_):
        if (not isinstance(F5HAi_Iv_, Pair)):
            return False
        return ((H_9G4L_X.Wai2 == F5HAi_Iv_.Wai2) and (H_9G4L_X.H7dNr_ == F5HAi_Iv_.H7dNr_))

    def map(H_9G4L_X, r2__13):
        'J3wv_189_7k3iK_393D4M013Gp45'
        C35U9C0 = r2__13(H_9G4L_X.Wai2)
        if ((H_9G4L_X.H7dNr_ is nil) or isinstance(H_9G4L_X.H7dNr_, Pair)):
            return Pair(C35U9C0, H_9G4L_X.H7dNr_.map(r2__13))
        else:
            raise TypeError(((('ill-formed list (cd' + 'r is a') + (' ' + 'promis')) + (chr(101) + ')')))

    def oJ_0(H_9G4L_X, r2__13):
        'W_19F1_x_H718t68C___F_a_'
        C35U9C0 = r2__13(H_9G4L_X.Wai2)
        if ((H_9G4L_X.H7dNr_ is nil) or isinstance(H_9G4L_X.H7dNr_, Pair)):
            return v7NLxX(C35U9C0, H_9G4L_X.H7dNr_.oJ_0(r2__13))
        else:
            raise TypeError(((('i' + 'll') + ('-formed list' + ' (cd')) + ('r' + (' i' + 's a promise)'))))

class nil(object):
    'ZP263916x27_5254__3Om'

    def __repr__(H_9G4L_X):
        return (str() + (str() + ('' + 'nil')))

    def __str__(H_9G4L_X):
        return (str() + (chr(40) + ')'))

    def __len__(H_9G4L_X):
        return int((((-0.41257998143389085 + 0.3460297556881715) + (0.13383359020547958 + 0.3316483249280179)) * int(((0.20779882674950612 + 0.33007403488331155) * int((0.31322902425271404 * 0))))))

    def map(H_9G4L_X, r2__13):
        return H_9G4L_X

    def oJ_0(H_9G4L_X, r2__13):
        return H_9G4L_X
nil = nil()
z_18O89 = {chr(((46 + -7) + int((0.40354281772354106 * 0)))): (('q' + ('uo' + 't')) + chr((114 + -13))), chr((72 + 24)): ((('' + 'qu') + ('as' + 'iquot')) + chr((128 + -27))), (str() + (chr(44) + chr(64))): ((('u' + 'n') + ('qu' + 'ote')) + (('-s' + 'pl') + ('icin' + 'g'))), chr(44): (str() + (('' + 'unquo') + ('' + 'te')))}

def Zb___69vz(kSv_H_9aX):
    'Z8_62hC_6o9sY5r41401_W'
    if (kSv_H_9aX.current() is None):
        raise EOFError
    vUx_63E = kSv_H_9aX.Xz9_yJj_()
    if (vUx_63E == (str() + ('' + ('' + 'nil')))):
        return nil
    elif (vUx_63E in set((chr((56 + -16)) + chr((84 + 7))))):
        if (kSv_H_9aX.current() == chr(((47 + -15) + (-60 + 74)))):
            raise SyntaxError((('' + ('. canno' + 't be ')) + (('the ' + 'first token in a l') + ('i' + 'st'))))
        return QZyB(kSv_H_9aX, vUx_63E, {'(': chr(((183 + -57) + (-72 + -13))), chr(((128 + -62) + (-25 + 50))): chr(((198 + -87) + (-72 + 54)))}[vUx_63E])
    elif (vUx_63E in z_18O89):
        return Pair(z_18O89[vUx_63E], Pair(Zb___69vz(kSv_H_9aX), nil))
    elif (vUx_63E not in x_ki):
        return vUx_63E
    else:
        raise SyntaxError(((('u' + 'n') + ('ex' + 'pe')) + (('' + 'cted ') + ('token: {' + '0}'))).format(vUx_63E))

def QZyB(kSv_H_9aX, w8n7_H72='(', QG26=')'):
    'U36E_040e_88_J_6k__h7r6_hIb_'
    try:
        if (kSv_H_9aX.current() is None):
            raise SyntaxError(((('un' + 'expecte') + ('d end o' + 'f')) + ((' fi' + 'l') + chr(101))))
        elif (kSv_H_9aX.current() in set((str() + ('' + ('' + ')]'))))):
            if (kSv_H_9aX.current() != QG26):
                raise SyntaxError(((('Exp' + 'ec') + ('ted' + ' {}')) + ((' to mat' + 'ch') + (' with' + ' {} but got {}'))).format(QG26, w8n7_H72, kSv_H_9aX.current()))
            kSv_H_9aX.Xz9_yJj_()
            return nil
        elif (kSv_H_9aX.current() == chr(((-101 + 77) + (34 + 36)))):
            kSv_H_9aX.Xz9_yJj_()
            G8y_e40 = Zb___69vz(kSv_H_9aX)
            if (kSv_H_9aX.current() is None):
                raise SyntaxError(((('' + 'unexpec') + ('ted en' + 'd')) + ((' of' + ' f') + ('' + 'ile'))))
            if (kSv_H_9aX.Xz9_yJj_() != chr(((123 + -86) + (63 + -59)))):
                raise SyntaxError(((('expected one ele' + 'men') + ('t' + ' ')) + (('afte' + 'r ') + chr(46))))
            if enIzy308_.DOTS_ARE_CONS:
                return G8y_e40
            else:
                return Pair(Pair((chr(118) + (chr(97) + ('' + 'riadic'))), Pair(G8y_e40, nil)), nil)
        else:
            Wai2 = Zb___69vz(kSv_H_9aX)
            H7dNr_ = QZyB(kSv_H_9aX, w8n7_H72, QG26)
            return Pair(Wai2, H7dNr_)
    except EOFError:
        raise SyntaxError(((('u' + 'nexpecte') + ('d' + ' ')) + (('end o' + 'f ') + ('' + 'file'))))

def kTx61Z_Yr(W276Q_='scm> '):
    'Y_215zd4vQ97DY_O_80_65M'
    return e50_T_22(f5_v2S(Pt06(W276Q_)))

def m_2XuJE(C3m_, W276Q_='scm> ', au4yoL_J6=False):
    'TU9D9k430wm__14q_855_69'
    if au4yoL_J6:
        C55z9 = C3m_
    else:
        C55z9 = wV33MCA_Y(C3m_, W276Q_)
    return e50_T_22(f5_v2S(C55z9))

def wJ__(x_77522):
    'Fo4V1_9X2a_sqtZ6jDuOu'
    rAC_7W6zX = e50_T_22(f5_v2S([x_77522]))
    bq9X9 = Zb___69vz(rAC_7W6zX)
    if rAC_7W6zX.WN0Y_:
        raise SyntaxError(((('rea' + "d_line's") + (' argu' + 'men')) + (('t can o' + 'nl') + ('y be a single element, but received m' + 'ultiple'))))
    return bq9X9

def repl_str(vUx_63E):
    'V06F1uS26_78x0m6W5Sq'
    if (vUx_63E is True):
        return (str() + ('#' + 't'))
    if (vUx_63E is False):
        return (str() + ('' + ('#' + 'f')))
    if (vUx_63E is None):
        return (('' + ('un' + 'define')) + chr((1 + 99)))
    if (isinstance(vUx_63E, c6bb_tj_.Number) and (not isinstance(vUx_63E, c6bb_tj_.Integral))):
        return repr(vUx_63E)
    return str(vUx_63E)

def b9w6r_():
    'G5C8M__0k_o6_k6ec1u3'
    while True:
        try:
            kSv_H_9aX = kTx61Z_Yr((str() + (('' + 'read>') + ' ')))
            while kSv_H_9aX.WN0Y_:
                F88t_nC = Zb___69vz(kSv_H_9aX)
                if (F88t_nC == ((str() + ('' + 'ex')) + ('' + ('' + 'it')))):
                    print()
                    return
                print((str() + (('' + 'str') + ('' + ' :'))), F88t_nC)
                print(((str() + ('' + 'rep')) + ('r' + ':')), repr(F88t_nC))
        except (SyntaxError, ValueError) as b7rvKk__:
            print((type(b7rvKk__).__name__ + ':'), b7rvKk__)
        except (KeyboardInterrupt, EOFError):
            print()
            return

def Ad4g(*EB1Tdm75):
    if (len(EB1Tdm75) and ((('-' + ('' + '-r')) + (('' + 'ep') + chr(108))) in EB1Tdm75)):
        b9w6r_()
'T31_0_7ZVNe6407TB516K__giyV_3'

class s600(Exception):
    'yB0upCNHrpo25k1_6I55900294A3'
B3tv9 = []

def I_x5_y3_(*C1qZ_Px06):
    'h73_H_143F_fET64D259y21e_62'

    def add(r2__13):
        for f__cU0_ in C1qZ_Px06:
            B3tv9.append((f__cU0_, r2__13, C1qZ_Px06[int((((-0.4232695258803232 + 0.43838734720679495) + (-0.41794951038578987 + 0.460777015527166)) * int((0.23694527155461065 * 0))))]))
        return r2__13
    return add

def K96a7_3X(vUx_63E, q2__, f_5K08, f__cU0_):
    'nH2GYDoUbdQ559g5_t92a16h73'
    if (not q2__(vUx_63E)):
        K01443 = ((('argu' + 'ment {0} of {1') + ('} has' + ' wro')) + (('ng ' + 'ty') + ('pe (' + '{2})')))
        c8_p718 = type(vUx_63E).__name__
        if T10r_5F_(vUx_63E):
            c8_p718 = (str() + (('' + 'sy') + ('mbo' + 'l')))
        raise s600(K01443.format(f_5K08, f__cU0_, c8_p718))
    return vUx_63E

@I_x5_y3_(((('bo' + 'o') + ('le' + 'a')) + ('n' + chr(63))))
def f67l_5(rPt_ajbd):
    return ((rPt_ajbd is True) or (rPt_ajbd is False))

def J3Zs5b(vUx_63E):
    'yp_1c_105y8J8_sq_8__0ud88__J6'
    return (vUx_63E is not False)

def m__28M6z4(vUx_63E):
    'j45S0M713_hE_8_3I05225_'
    return (vUx_63E is False)

@I_x5_y3_(('n' + ('' + ('' + 'ot'))))
def JN2n3163_(rPt_ajbd):
    return (not J3Zs5b(rPt_ajbd))

@I_x5_y3_(((('e' + 'q') + 'u') + (('' + 'al') + chr(63))))
def s2E4w7O0(rPt_ajbd, QXIjjD_6k):
    if (hmMM9(rPt_ajbd) and hmMM9(QXIjjD_6k)):
        return (s2E4w7O0(rPt_ajbd.Wai2, QXIjjD_6k.Wai2) and s2E4w7O0(rPt_ajbd.H7dNr_, QXIjjD_6k.H7dNr_))
    elif (e_76(rPt_ajbd) and e_76(QXIjjD_6k)):
        return (rPt_ajbd == QXIjjD_6k)
    else:
        return ((type(rPt_ajbd) == type(QXIjjD_6k)) and (rPt_ajbd == QXIjjD_6k))

@I_x5_y3_((('' + ('e' + 'q')) + chr((88 + -25))))
def s_bEA7fo8(rPt_ajbd, QXIjjD_6k):
    if (e_76(rPt_ajbd) and e_76(QXIjjD_6k)):
        return (rPt_ajbd == QXIjjD_6k)
    elif (T10r_5F_(rPt_ajbd) and T10r_5F_(QXIjjD_6k)):
        return (rPt_ajbd == QXIjjD_6k)
    else:
        return (rPt_ajbd is QXIjjD_6k)

@I_x5_y3_((('p' + ('ai' + 'r')) + chr((15 + 48))))
def hmMM9(rPt_ajbd):
    return (type(rPt_ajbd).__name__ == (chr(80) + (('a' + 'i') + chr(114))))

@I_x5_y3_(((('s' + 'ch') + ('eme-' + 'v')) + (('' + 'alid-cdr') + '?')))
def M5_8uB(rPt_ajbd):
    return (hmMM9(rPt_ajbd) or uF__(rPt_ajbd) or kC11(rPt_ajbd))

@I_x5_y3_(('' + (('pro' + 'm') + ('' + 'ise?'))))
def kC11(rPt_ajbd):
    return (type(rPt_ajbd).__name__ == (('' + ('' + 'Pr')) + (('' + 'omis') + chr(101))))

@I_x5_y3_((chr((35 + 67)) + (('o' + 'rc') + chr(101))))
def XZs0(rPt_ajbd):
    K96a7_3X(rPt_ajbd, kC11, int(((-0.19479485525405105 + 0.4651629061724445) * int((0.1880625096927765 * 0)))), (chr((31 + 81)) + (str() + ('rom' + 'ise'))))
    return rPt_ajbd.V_15()

@I_x5_y3_(((('' + 'cdr-') + ('s' + 't')) + (('r' + 'ea') + 'm')))
def g55Ed9(rPt_ajbd):
    K96a7_3X(rPt_ajbd, (lambda rPt_ajbd: (hmMM9(rPt_ajbd) and kC11(rPt_ajbd.H7dNr_))), int((((-0.8697667040279081 + 0.6370184866007303) + (-0.16598540180711185 + 0.715053662437789)) * int((0.00931279511155636 * 0)))), ((chr(99) + ('d' + 'r')) + ('-' + ('s' + 'tream'))))
    return XZs0(rPt_ajbd.H7dNr_)

@I_x5_y3_((('' + ('' + 'nu')) + ('l' + ('' + 'l?'))))
def uF__(rPt_ajbd):
    return (type(rPt_ajbd).__name__ == (chr((151 + -41)) + (chr(105) + chr(108))))

@I_x5_y3_(('l' + (('' + 'is') + ('t' + '?'))))
def Gm_Xir(rPt_ajbd):
    'XbZJ0w_0_1oh5c98g8_A80'
    while (rPt_ajbd is not nil):
        if (not isinstance(rPt_ajbd, Pair)):
            return False
        rPt_ajbd = rPt_ajbd.H7dNr_
    return True

@I_x5_y3_((('' + ('l' + 'e')) + (str() + ('ng' + 'th'))))
def Xo_ZZE_E(rPt_ajbd):
    K96a7_3X(rPt_ajbd, Gm_Xir, int((0.6909720043061245 * 0)), ((('l' + 'e') + 'n') + (('g' + 't') + 'h')))
    if (rPt_ajbd is nil):
        return int((((-0.9916083911187507 + 0.40494553281733114) + (0.8694845631840495 + 0.058533467697686525)) * int((0.46533473851079943 * 0))))
    return len(rPt_ajbd)

@I_x5_y3_(((chr(99) + 'o') + ('' + ('n' + 's'))))
def a3_L_(rPt_ajbd, QXIjjD_6k):
    return Pair(rPt_ajbd, QXIjjD_6k)

@I_x5_y3_((chr((68 + 31)) + ('a' + 'r')))
def QI__(rPt_ajbd):
    K96a7_3X(rPt_ajbd, hmMM9, int((((-0.7893084878422078 + 0.8103940672599927) + (0.2380390208751625 + 0.4917570165698425)) * int(((0.02591317917073599 + 0.17896512943487253) * 0)))), (chr(99) + (chr(97) + chr(114))))
    return rPt_ajbd.Wai2

@I_x5_y3_((str() + (('' + 'cd') + 'r')))
def W5W_T6__h(rPt_ajbd):
    K96a7_3X(rPt_ajbd, hmMM9, int((((-0.9097051199397006 + 0.5130814474261818) + (-0.49385781028305775 + 0.9456822188307696)) * int(((-0.089498341963965 + 0.11597798132387449) * 0)))), (('' + ('c' + 'd')) + chr(114)))
    return rPt_ajbd.H7dNr_

@I_x5_y3_(((('s' + 'e') + ('t' + '-ca')) + (chr(114) + '!')))
def DVnd_(rPt_ajbd, QXIjjD_6k):
    K96a7_3X(rPt_ajbd, hmMM9, int((((0.1254687473949858 + 0.03206800221069428) + (-0.4397498133130413 + 0.7057657690766097)) * int((0.21185092292563412 * 0)))), (('' + ('' + 'set')) + (('' + '-ca') + ('' + 'r!'))))
    rPt_ajbd.Wai2 = QXIjjD_6k

@I_x5_y3_((chr(115) + (('' + 'et-c') + ('d' + 'r!'))))
def M22L(rPt_ajbd, QXIjjD_6k):
    K96a7_3X(rPt_ajbd, hmMM9, int((((-0.8990216179169538 + 0.49009832008423715) + (-0.25085693523782604 + 0.6787680878210863)) * int(((0.19950817961647893 + 0.5322610429820491) * int((0.6599693358021381 * 0)))))), ('s' + ('' + ('et-cd' + 'r!'))))
    if (not enIzy308_.DOTS_ARE_CONS):
        K96a7_3X(QXIjjD_6k, M5_8uB, (((149 + -36) + (-18 + -66)) + ((-20 + 89) + (-109 + 12))), (('s' + chr(101)) + (('t' + '-cd') + ('' + 'r!'))))
    rPt_ajbd.H7dNr_ = QXIjjD_6k

@I_x5_y3_(('l' + (('' + 'is') + 't')))
def md3tap9m(*BFq2H8q):
    bq9X9 = nil
    for K_2f5Wj__ in reversed(BFq2H8q):
        bq9X9 = Pair(K_2f5Wj__, bq9X9)
    return bq9X9

@I_x5_y3_((str() + (('a' + 'pp') + ('e' + 'nd'))))
def v7NLxX(*BFq2H8q):
    if (len(BFq2H8q) == int((((-0.24586550904405668 + 0.06489886776305331) + (-0.442017234780849 + 0.8328208015024597)) * int(((-0.1811215453051268 + 0.23912364241407658) * 0))))):
        return nil
    bq9X9 = BFq2H8q[(- (((65 + 4) + (-56 + 83)) + ((-66 + -81) + (122 + -70))))]
    for VE28Mj in range((len(BFq2H8q) - (((-193 + 36) + (168 + -99)) + ((123 + 29) + (4 + -66)))), (- (((30 + 59) + (-65 + 10)) + ((42 + -6) + (-132 + 63)))), (- (((-38 + 63) + (-27 + 87)) + ((-131 + 54) + (52 + -59))))):
        q5Y3900g = BFq2H8q[VE28Mj]
        if (q5Y3900g is not nil):
            K96a7_3X(q5Y3900g, hmMM9, VE28Mj, ((('' + 'ap') + ('' + 'pe')) + (chr(110) + 'd')))
            Ioda = F5HAi_Iv_ = Pair(q5Y3900g.Wai2, bq9X9)
            q5Y3900g = q5Y3900g.H7dNr_
            while hmMM9(q5Y3900g):
                F5HAi_Iv_.H7dNr_ = Pair(q5Y3900g.Wai2, bq9X9)
                F5HAi_Iv_ = F5HAi_Iv_.H7dNr_
                q5Y3900g = q5Y3900g.H7dNr_
            bq9X9 = Ioda
    return bq9X9

@I_x5_y3_((('' + ('' + 'st')) + (str() + ('ring' + '?'))))
def E_I3(rPt_ajbd):
    return (isinstance(rPt_ajbd, str) and rPt_ajbd.startswith(chr((5 + 29))))

@I_x5_y3_(((chr(115) + ('y' + 'mb')) + (str() + ('ol' + '?'))))
def T10r_5F_(rPt_ajbd):
    return (isinstance(rPt_ajbd, str) and (not E_I3(rPt_ajbd)))

def A_3b18(rPt_ajbd):
    return (Gm_Xir(rPt_ajbd) and (Xo_ZZE_E(rPt_ajbd) == (((120 + -59) + (-9 + -34)) + ((-152 + 92) + (74 + -30)))) and (rPt_ajbd.Wai2 == ((('v' + 'ar') + ('' + 'iad')) + (str() + ('i' + 'c')))) and T10r_5F_(rPt_ajbd.H7dNr_.Wai2))

def P_7tpp45(rPt_ajbd):
    assert A_3b18(rPt_ajbd)
    return rPt_ajbd.H7dNr_.Wai2

@I_x5_y3_(((str() + ('n' + 'um')) + (str() + ('be' + 'r?'))))
def e_76(rPt_ajbd):
    return (isinstance(rPt_ajbd, c6bb_tj_.Real) and (not f67l_5(rPt_ajbd)))

@I_x5_y3_(('' + (('i' + 'ntege') + ('' + 'r?'))))
def I09_(rPt_ajbd):
    return (e_76(rPt_ajbd) and (isinstance(rPt_ajbd, c6bb_tj_.Integral) or (int(rPt_ajbd) == rPt_ajbd)))

def w95lK86x5(*BFq2H8q):
    'O71kb2Z224D1a11L8e7L2_OA9_57'
    for (VE28Mj, q5Y3900g) in enumerate(BFq2H8q):
        if (not e_76(q5Y3900g)):
            K01443 = ((('o' + 'perand {0') + ('} ({1}) is' + ' no')) + ('' + ('t a nu' + 'mber')))
            raise s600(K01443.format(VE28Mj, q5Y3900g))

def ppPTh1__(r2__13, R13W06xK2, BFq2H8q):
    'g7N9_614b2m545QYC_1_f'
    w95lK86x5(*BFq2H8q)
    P_7q887A_ = R13W06xK2
    for vUx_63E in BFq2H8q:
        P_7q887A_ = r2__13(P_7q887A_, vUx_63E)
    P_7q887A_ = WU_2UR_2m(P_7q887A_)
    return P_7q887A_

def WU_2UR_2m(rPt_ajbd):
    if (int(rPt_ajbd) == rPt_ajbd):
        rPt_ajbd = int(rPt_ajbd)
    return rPt_ajbd

@I_x5_y3_(chr(((166 + -74) + (25 + -74))))
def Jcz781G_E(*BFq2H8q):
    return ppPTh1__(V72R6_47.add, int(((0.4445659672456378 + 0.3218315556103831) * 0)), BFq2H8q)

@I_x5_y3_(chr((12 + 33)))
def x_3_s(J_a_4mO_0, *BFq2H8q):
    w95lK86x5(J_a_4mO_0, *BFq2H8q)
    if (len(BFq2H8q) == int(((0.1495252583827953 + 0.6040804290851023) * int((0.6808746478784761 * 0))))):
        return WU_2UR_2m((- J_a_4mO_0))
    return ppPTh1__(V72R6_47.sub, J_a_4mO_0, BFq2H8q)

@I_x5_y3_(chr((78 + -36)))
def G4i7s6_X(*BFq2H8q):
    return ppPTh1__(V72R6_47.mul, (((32 + -90) + (3 + 72)) + ((-43 + 42) + (71 + -86))), BFq2H8q)

@I_x5_y3_(chr((131 + -84)))
def Fk2Y_70Ds(J_a_4mO_0, *BFq2H8q):
    w95lK86x5(J_a_4mO_0, *BFq2H8q)
    try:
        if (len(BFq2H8q) == int(((0.4286662625986225 + 0.17446198132091773) * 0))):
            return WU_2UR_2m(V72R6_47.truediv((((72 + -96) + (-54 + 65)) + ((-109 + 92) + (48 + -17))), J_a_4mO_0))
        return ppPTh1__(V72R6_47.truediv, J_a_4mO_0, BFq2H8q)
    except ZeroDivisionError as b7rvKk__:
        raise s600(b7rvKk__)

@I_x5_y3_(((('e' + 'x') + chr(112)) + chr(116)))
def r3yp(J_a_4mO_0, w_3y_Crlj):
    w95lK86x5(J_a_4mO_0, w_3y_Crlj)
    return pow(J_a_4mO_0, w_3y_Crlj)

@I_x5_y3_((chr((168 + -71)) + (chr(98) + chr(115))))
def w_B8X2(J_a_4mO_0):
    return abs(J_a_4mO_0)

@I_x5_y3_(((('quot' + 'i') + chr(101)) + (str() + ('' + 'nt'))))
def DeQnR(J_a_4mO_0, w_3y_Crlj):
    w95lK86x5(J_a_4mO_0, w_3y_Crlj)
    try:
        return ((- ((- J_a_4mO_0) // w_3y_Crlj)) if ((J_a_4mO_0 < int((((-0.7596093539998686 + 0.33365837545132393) + (-0.05191277176734932 + 0.6683825137904466)) * int(((-0.11346296165785097 + 0.953616237783876) * int((0.4987112836606984 * 0))))))) ^ (w_3y_Crlj < int(((-0.35409735909641893 + 0.47307782338679527) * int((0.20371380855919485 * 0)))))) else (J_a_4mO_0 // w_3y_Crlj))
    except ZeroDivisionError as b7rvKk__:
        raise s600(b7rvKk__)

@I_x5_y3_((('' + ('modu' + 'l')) + chr((36 + 75))))
def TWD_09(J_a_4mO_0, w_3y_Crlj):
    w95lK86x5(J_a_4mO_0, w_3y_Crlj)
    try:
        return (J_a_4mO_0 % w_3y_Crlj)
    except ZeroDivisionError as b7rvKk__:
        raise s600(b7rvKk__)

@I_x5_y3_(((str() + ('' + 're')) + (('' + 'maind') + ('' + 'er'))))
def vnzx2_(J_a_4mO_0, w_3y_Crlj):
    w95lK86x5(J_a_4mO_0, w_3y_Crlj)
    try:
        bq9X9 = (J_a_4mO_0 % w_3y_Crlj)
    except ZeroDivisionError as b7rvKk__:
        raise s600(b7rvKk__)
    while (((bq9X9 < int((((-1.0262577617687658 + 0.5677396905465698) + (0.31341381347379493 + 0.617916635846979)) * int(((-0.6371142179832516 + 0.8972942515613307) * int((0.916449254320227 * 0))))))) and (J_a_4mO_0 > int((((-0.3787502225996925 + 0.25647071447789904) + (0.3485098890027548 + 0.30606475109119)) * int((0.2948030938356645 * 0)))))) or ((bq9X9 > int(((0.416106881975721 + 0.4453198031766119) * 0))) and (J_a_4mO_0 < int(((-0.43050268164523353 + 0.49795081744387804) * int((0.4140077408367957 * 0))))))):
        bq9X9 -= w_3y_Crlj
    return bq9X9

def u_029_stm(B96_jm7, f__cU0_, R_Sxr5m8k=None):
    'b7M07TAq2_0L30_95X8s7s0'
    M_4R2 = (getattr(B96_jm7, f__cU0_) if (R_Sxr5m8k is None) else getattr(B96_jm7, f__cU0_, R_Sxr5m8k))

    def h__6ddz(*BFq2H8q):
        w95lK86x5(*BFq2H8q)
        return M_4R2(*BFq2H8q)
    return h__6ddz
for D_9r_3D2 in [((str() + ('ac' + 'o')) + chr((18 + 97))), ((('ac' + 'o') + chr(115)) + chr(104)), (str() + (('' + 'as') + ('i' + 'n'))), (('' + ('a' + 'sin')) + 'h'), ('' + (chr(97) + ('ta' + 'n'))), ((('a' + 't') + 'a') + ('' + ('n' + '2'))), ((('a' + 't') + 'a') + (str() + ('' + 'nh'))), (('' + ('ce' + 'i')) + chr((119 + -11))), ((('' + 'co') + ('' + 'pysi')) + ('' + ('' + 'gn'))), (chr(99) + ('o' + 's')), ((chr(99) + ('' + 'os')) + chr(104)), (chr((53 + 47)) + ('e' + ('gree' + 's'))), (chr(102) + (('' + 'lo') + ('' + 'or'))), (str() + ('' + ('' + 'log'))), ((str() + ('' + 'log')) + ('1' + chr(48))), (('' + ('l' + 'og')) + ('1' + 'p')), ((('r' + 'a') + chr(100)) + (('i' + 'a') + ('n' + 's'))), (chr((208 + -93)) + (chr(105) + chr(110))), (('' + ('s' + 'i')) + ('' + ('' + 'nh'))), (chr((129 + -14)) + (chr(113) + ('r' + 't'))), (str() + (('' + 'ta') + chr(110))), (chr((200 + -84)) + (('' + 'an') + chr(104))), (chr(116) + ('r' + ('un' + 'c')))]:
    I_x5_y3_(D_9r_3D2)(u_029_stm(y4C7, D_9r_3D2))
I_x5_y3_((('' + ('l' + 'o')) + ('' + ('' + 'g2'))))(u_029_stm(y4C7, (chr(108) + (('o' + 'g') + '2')), (lambda rPt_ajbd: y4C7.log(rPt_ajbd, (((46 + -24) + (9 + -91)) + ((177 + -97) + (-90 + 72)))))))

def A4___8_s9(Lv58E, rPt_ajbd, QXIjjD_6k):
    w95lK86x5(rPt_ajbd, QXIjjD_6k)
    return Lv58E(rPt_ajbd, QXIjjD_6k)

@I_x5_y3_(chr(((212 + -88) + (-16 + -47))))
def k47_(rPt_ajbd, QXIjjD_6k):
    return A4___8_s9(V72R6_47.eq, rPt_ajbd, QXIjjD_6k)

@I_x5_y3_(chr(((-103 + 68) + (106 + -11))))
def qX84k(rPt_ajbd, QXIjjD_6k):
    return A4___8_s9(V72R6_47.lt, rPt_ajbd, QXIjjD_6k)

@I_x5_y3_(chr(((163 + -69) + (-75 + 43))))
def s_uZ490_x(rPt_ajbd, QXIjjD_6k):
    return A4___8_s9(V72R6_47.gt, rPt_ajbd, QXIjjD_6k)

@I_x5_y3_((str() + ('<' + chr(61))))
def Qu32h2(rPt_ajbd, QXIjjD_6k):
    return A4___8_s9(V72R6_47.le, rPt_ajbd, QXIjjD_6k)

@I_x5_y3_((chr((133 + -71)) + chr(61)))
def Qq3F(rPt_ajbd, QXIjjD_6k):
    return A4___8_s9(V72R6_47.ge, rPt_ajbd, QXIjjD_6k)

@I_x5_y3_(((('e' + 'v') + chr(101)) + ('' + ('' + 'n?'))))
def k524E_6r3(rPt_ajbd):
    w95lK86x5(rPt_ajbd)
    return ((rPt_ajbd % (((8 + 42) + (-35 + 43)) + ((39 + -84) + (78 + -89)))) == int((((-0.3156420227953569 + 0.6177387680739108) + (-0.21295993694072157 + 0.351086986638632)) * int(((0.19605284742073448 + 0.6034418159095953) * 0)))))

@I_x5_y3_((str() + ('' + ('od' + 'd?'))))
def k6x23x_M(rPt_ajbd):
    w95lK86x5(rPt_ajbd)
    return ((rPt_ajbd % (((178 + -85) + (-18 + -69)) + ((17 + -87) + (-25 + 91)))) == (((-212 + 65) + (189 + -93)) + ((187 + -83) + (-84 + 32))))

@I_x5_y3_(((('' + 'ze') + chr(114)) + ('o' + '?')))
def f_8k8(rPt_ajbd):
    w95lK86x5(rPt_ajbd)
    return (rPt_ajbd == int((((-1.341373588120846 + 0.9182564451995738) + (0.2698195308615836 + 0.38072772090860807)) * int((0.02439576697166257 * 0)))))

@I_x5_y3_(((chr(97) + 't') + (str() + ('om' + '?'))))
def ltJ2(rPt_ajbd):
    return (f67l_5(rPt_ajbd) or e_76(rPt_ajbd) or T10r_5F_(rPt_ajbd) or uF__(rPt_ajbd) or E_I3(rPt_ajbd))

@I_x5_y3_((('d' + ('is' + 'pl')) + (chr(97) + 'y')))
def zdE__4g9(*BFq2H8q):
    BFq2H8q = [repl_str((eval(vUx_63E) if E_I3(vUx_63E) else vUx_63E)) for vUx_63E in BFq2H8q]
    print(*BFq2H8q, end=str())

@I_x5_y3_((chr(112) + (chr(114) + ('' + 'int'))))
def eO_br76(*BFq2H8q):
    BFq2H8q = [repl_str(vUx_63E) for vUx_63E in BFq2H8q]
    print(*BFq2H8q)

@I_x5_y3_(((chr(100) + ('ispla' + 'yl')) + chr((70 + 40))))
def H4c_U43(*BFq2H8q):
    zdE__4g9(*BFq2H8q)
    j_6qE()

@I_x5_y3_(((('' + 'ne') + chr(119)) + (('' + 'li') + ('n' + 'e'))))
def j_6qE():
    print()
    L5948Fbo.stdout.flush()

@I_x5_y3_((chr((44 + 57)) + (str() + ('rro' + 'r'))))
def hU6_d38(K01443=None):
    K01443 = (str() if (K01443 is None) else repl_str(K01443))
    raise s600(K01443)

@I_x5_y3_((('e' + ('x' + 'i')) + 't'))
def y7i06ua():
    raise EOFError
bw6b = qL__m7__ = None

def yo74brdY():
    import turtle as q2r6161
    q2r6161.title((str() + (('Scheme Tu' + 'rtl') + ('e' + 's'))))

def n23R6():
    try:
        from abstract_turtle import turtle as bw6b
    except ImportError:
        raise s600(((('Could not find abstract_turtle. This should never happen in student-facing situations. ' + 'If you ar') + ('e' + ' a student, please file a bug on Pi')) + (chr(97) + ('z' + 'za.'))))
    return bw6b

def fb_RtS12():
    try:
        import tkinter as x_x07
    except:
        raise s600(chr(((41 + -3) + (28 + -56))).join([((('' + 'Cou') + ('ld not ' + 'impo')) + (('rt' + ' t') + ('kinter, so the tk-turtle will' + ' not work.'))), ((('Eith' + 'er install python ') + ('with t' + 'kinter support or run in pillow')) + (('-' + 'turtl') + ('e ' + 'mode')))]))
    from abstract_turtle import TkCanvas as JuLF
    return JuLF((((1049 + -32) + (-91 + 23)) + ((-111 + 94) + (76 + -8))), (((1043 + 94) + (-26 + -22)) + ((-154 + 100) + (21 + -56))), init_hook=yo74brdY)

def P6T0ed():
    try:
        import PIL as x_x07
        import numpy as x_x07
    except:
        raise s600(chr(((-34 + 39) + (101 + -96))).join([((('C' + 'ould n') + ('ot ' + 'impor')) + (('' + 't abstract_turtle[pillow_ca') + ('nvas' + "]'s dependencies."))), ((('' + 'To') + ('' + ' install')) + ((' these pac' + 'k') + ('' + 'ages, run'))), ((' ' + ' ') + (('  python3 -' + "m pip install 'abstra") + ('ct_' + "turtle[pillow_canvas]'"))), ((('You can also run in tk-turtle m' + 'ode') + (' by removing the flag `--pil' + 'low-')) + (str() + ('turtl' + 'e`')))]))
    from abstract_turtle import PillowCanvas as A80g19_6
    return A80g19_6((((977 + 79) + (43 + -15)) + ((-209 + 54) + (72 + -1))), (((969 + 74) + (-27 + -68)) + ((30 + 100) + (-20 + -58))))

def EcW7R_0_():
    global bw6b, qL__m7__
    if (bw6b is not None):
        return
    x1FK = n23R6()
    if enIzy308_.TK_TURTLE:
        try:
            T69tO1 = fb_RtS12()
        except s600 as K_2f5Wj__:
            print(K_2f5Wj__, file=L5948Fbo.stderr)
            print(((('' + 'Atte') + chr(109)) + (('p' + 'ting pil') + ('low canvas mo' + 'de'))), file=L5948Fbo.stderr)
            T69tO1 = P6T0ed()
    else:
        T69tO1 = P6T0ed()
    (bw6b, qL__m7__) = (x1FK, T69tO1)
    bw6b.set_canvas(qL__m7__)
    bw6b.mode(((chr(108) + 'o') + ('g' + chr(111))))

@I_x5_y3_(((str() + ('for' + 'war')) + chr(100)), (str() + ('' + ('' + 'fd'))))
def z1fd(e___6V_):
    's_S5Otcq2_1G09X3__R_Kc7E57dax'
    w95lK86x5(e___6V_)
    EcW7R_0_()
    bw6b.forward(e___6V_)

@I_x5_y3_(((str() + ('b' + 'a')) + ('c' + ('kw' + 'ard'))), (str() + (('b' + 'ac') + chr(107))), (chr(98) + 'k'))
def N7Xv40(e___6V_):
    'J14G_7O2_74c2_4_1T_81zJ'
    w95lK86x5(e___6V_)
    EcW7R_0_()
    bw6b.backward(e___6V_)

@I_x5_y3_((chr((172 + -64)) + (('e' + 'f') + 't')), (chr((153 + -45)) + chr(116)))
def Tfk157(e___6V_):
    'SC_we316X9dU9T1h00VgF0_6l_u2'
    w95lK86x5(e___6V_)
    EcW7R_0_()
    bw6b.left(e___6V_)

@I_x5_y3_((str() + (('rig' + 'h') + 't')), (chr((160 + -46)) + 't'))
def B87_(e___6V_):
    'p5N86Y1___i__3q_0_Xju_SS'
    w95lK86x5(e___6V_)
    EcW7R_0_()
    bw6b.right(e___6V_)

@I_x5_y3_(((('' + 'ci') + chr(114)) + (('' + 'cl') + chr(101))))
def CM96_78(Ioda, V35mw54=None):
    'mTy_77v3_c_abUd_LwfPRTLz'
    if (V35mw54 is None):
        w95lK86x5(Ioda)
    else:
        w95lK86x5(Ioda, V35mw54)
    EcW7R_0_()
    bw6b.circle(Ioda, (V35mw54 and V35mw54))

@I_x5_y3_(((str() + ('' + 'se')) + (('t' + 'p') + ('o' + 'sition'))), ((str() + ('se' + 'tp')) + ('' + ('o' + 's'))), ('' + ('g' + ('' + 'oto'))))
def s_238(rPt_ajbd, QXIjjD_6k):
    'D601_8Bad28___y_L_Q62I1H'
    w95lK86x5(rPt_ajbd, QXIjjD_6k)
    EcW7R_0_()
    bw6b.setposition(rPt_ajbd, QXIjjD_6k)

@I_x5_y3_(((str() + ('' + 'sethead')) + (('i' + 'n') + chr(103))), ((str() + ('s' + 'e')) + (chr(116) + 'h')))
def q6Ks(U_t__5__7):
    'i1up_Z3Ma__6c__m568V_Y7h'
    w95lK86x5(U_t__5__7)
    EcW7R_0_()
    bw6b.setheading(U_t__5__7)

@I_x5_y3_(((chr(112) + chr(101)) + (('' + 'nu') + 'p')), (chr((91 + 21)) + chr((171 + -54))))
def v948396():
    'YDtl5__PpO1L2Nm7J8k__5w8_k_'
    EcW7R_0_()
    bw6b.penup()

@I_x5_y3_(((('pe' + 'n') + ('d' + 'ow')) + chr((176 + -66))), (str() + (str() + ('p' + 'd'))))
def YWw3Mt53_():
    'U90H6139_Iksy2xJ7Z_U'
    EcW7R_0_()
    bw6b.pendown()

@I_x5_y3_(((chr(115) + chr(104)) + (('o' + 'w') + ('turtl' + 'e'))), (chr(115) + chr((142 + -26))))
def GF375_O1():
    'y313____Y5R_6_MM_69hK'
    EcW7R_0_()
    bw6b.showturtle()

@I_x5_y3_(((str() + ('' + 'hi')) + (chr(100) + ('' + 'eturtle'))), (chr(104) + 't'))
def gng_y():
    'XrpG426cJWa_S_j6_6M0T50M'
    EcW7R_0_()
    bw6b.hideturtle()

@I_x5_y3_((str() + ('' + ('clea' + 'r'))))
def t_2p():
    'vw_ZE42g98L614_4Yxx72c2b4k7_'
    EcW7R_0_()
    bw6b.clear()

@I_x5_y3_(('' + (('c' + 'o') + ('' + 'lor'))))
def vw40A65x_(z78_8_z_):
    'Zq_c3pnSQ_7_6__PTI9_8VR_o'
    EcW7R_0_()
    K96a7_3X(z78_8_z_, E_I3, int((((-1.3441424057401927 + 0.6094051587960431) + (0.7916611562013282 + 0.1794989676400618)) * int(((-0.24822267622211402 + 0.7186960234065674) * int((0.5674243910741003 * 0)))))), ('c' + (('' + 'ol') + ('' + 'or'))))
    bw6b.color(eval(z78_8_z_))

@I_x5_y3_(('' + (('' + 'rg') + chr(98))))
def tZM__x(T983V_, S5QE, Q87kn2x):
    'jq_X_hY35DCY4__9k2KV1'
    Yx5y3 = (T983V_, S5QE, Q87kn2x)
    for rPt_ajbd in Yx5y3:
        if ((rPt_ajbd < int((((-0.6785816301634877 + 0.378989665312607) + (0.709957201653813 + 0.23480341691389817)) * int(((0.16688778330033582 + 0.7436689655144707) * int((0.07046047214628792 * 0))))))) or (rPt_ajbd > (((-39 + -70) + (39 + -28)) + ((127 + -80) + (-38 + 90))))):
            raise s600((((('Ille' + 'gal color ') + ('i' + 'ntensity')) + ('' + (' i' + 'n '))) + repl_str(Yx5y3)))
    QE4DIz_4 = tuple((int((rPt_ajbd * (((100 + 83) + (82 + -1)) + ((47 + 21) + (-113 + 36))))) for rPt_ajbd in Yx5y3))
    return (((('' + '"#%02') + ('' + 'x%02x%')) + (str() + ('' + '02x"'))) % QE4DIz_4)

@I_x5_y3_(((str() + ('beg' + 'i')) + (('n_fi' + 'l') + chr(108))))
def j3o_26_():
    'MkZ8o_0UFHCv7dM_9__a0vyiW1k'
    EcW7R_0_()
    bw6b.begin_fill()

@I_x5_y3_((('e' + chr(110)) + (chr(100) + ('_fi' + 'll'))))
def j9A__406s():
    'dyo__80J5_0UU6i_5LKD'
    EcW7R_0_()
    bw6b.end_fill()

@I_x5_y3_(((chr(98) + ('' + 'gcolo')) + chr((117 + -3))))
def rIV7l_h(z78_8_z_):
    EcW7R_0_()
    K96a7_3X(z78_8_z_, E_I3, int((((-0.49174999867125224 + 0.1475369038865555) + (0.4535619070977499 + 0.24856118700506669)) * 0)), (str() + (('bgc' + 'ol') + ('' + 'or'))))
    bw6b.bgcolor(eval(z78_8_z_))

@I_x5_y3_((str() + (('exi' + 'to') + ('nc' + 'lick'))))
def A255ea8():
    global bw6b
    'fRWH5rz1h_5P36Rw85_B_7f06Lt'
    if (bw6b is None):
        return
    EcW7R_0_()
    if enIzy308_.TK_TURTLE:
        print(((('Close or click on turtle ' + 'window') + (' to co' + 'mplete')) + ((' ex' + 'i') + chr(116))))
    if (enIzy308_.TURTLE_SAVE_PATH is not None):
        I_OX_74Z(enIzy308_.TURTLE_SAVE_PATH)
    bw6b.exitonclick()
    bw6b = None

@I_x5_y3_((chr((174 + -59)) + (str() + ('' + 'peed'))))
def ZH_IuB(P_7q887A_):
    'Tw103m_Ml_7n_Ld__L72Rq'
    K96a7_3X(P_7q887A_, I09_, int((((-0.6370592273420836 + 0.9772473766898497) + (-0.3802863503666133 + 0.8929033352223296)) * int(((-0.36209036342312406 + 0.5737146971230642) * 0)))), (str() + (('s' + 'pee') + chr(100))))
    EcW7R_0_()
    bw6b.speed(P_7q887A_)

@I_x5_y3_(((chr(112) + ('i' + 'x')) + ('' + ('' + 'el'))))
def GS__YTv1(rPt_ajbd, QXIjjD_6k, z78_8_z_):
    'PpH4pS5l_Q29e1_ram23o2'
    K96a7_3X(z78_8_z_, E_I3, 0, (str() + (chr(112) + ('i' + 'xel'))))
    aiGO = eval(z78_8_z_)
    EcW7R_0_()
    bw6b.pixel(rPt_ajbd, QXIjjD_6k, aiGO)

@I_x5_y3_(((('' + 'pi') + 'x') + ('e' + ('lsiz' + 'e'))))
def y4_42av(t2__1__):
    'Wi5__DoOu8NI666u8NV0R_8'
    w95lK86x5(t2__1__)
    EcW7R_0_()
    bw6b.pixel_size(t2__1__)

@I_x5_y3_(((str() + ('screen_' + 'wi')) + (str() + ('d' + 'th'))))
def v7_Y():
    'kM8u_8___nZWr_ZYi6E4vdkm'
    EcW7R_0_()
    return bw6b.canvas_width()

@I_x5_y3_(((('s' + 'c') + ('' + 'ree')) + (('' + 'n_hei') + ('g' + 'ht'))))
def QaUXNm62():
    'k1_eU8___ax66166_y_t5_'
    EcW7R_0_()
    return bw6b.canvas_height()

def I_OX_74Z(K28wk0):
    if (not enIzy308_.TK_TURTLE):
        K28wk0 = (K28wk0 + ('' + ('.' + ('' + 'png'))))
        qL__m7__.export().save(K28wk0, (chr(112) + (str() + ('n' + 'g'))))
    else:
        qL__m7__.export((K28wk0 + ((chr(46) + 'p') + chr(115))))

@I_x5_y3_((('s' + ('ave' + '-to-')) + (('fi' + 'l') + chr(101))))
def nv7988JW(K28wk0):
    EcW7R_0_()
    K96a7_3X(K28wk0, E_I3, 0, ((str() + ('' + 'save-')) + ('t' + ('o' + '-file'))))
    K28wk0 = eval(K28wk0)
    I_OX_74Z(K28wk0)
'u_6_v_tNe_63jrMd1D77t0n_j'
It1__S71 = (set(string.digits) | set(('' + ('+' + ('-' + '.')))))
C3f8S3c = (((set(((('!' + '$%&*') + ('/:<=>?@' + '^_')) + chr(126))) | set(string.ascii_lowercase)) | set(string.ascii_uppercase)) | It1__S71)
Yq1jCeV = set(chr(((-9 + -50) + (61 + 32))))
wt45LpX = set((str() + (str() + ('' + ' \t\n\r'))))
F4K748__ = set((str() + (('' + '()') + ('' + "[]'`"))))
UYz43 = (((wt45LpX | F4K748__) | Yq1jCeV) | {chr(((65 + -86) + (43 + 22))), (chr((-52 + 96)) + chr((11 + 53)))})
x_ki = (F4K748__ | {chr(((-19 + 9) + (29 + 27))), chr(((201 + -71) + (-126 + 40))), ('' + ('' + (',' + '@')))})

def xXk6F(P_7q887A_):
    'gJ6X__R04306F938LAB5E_S95q_Q'
    if (len(P_7q887A_) == int(((-0.01625206722390027 + 0.10101538232924967) * 0))):
        return False
    for z78_8_z_ in P_7q887A_:
        if (z78_8_z_ not in C3f8S3c):
            return False
    return True

def t5_z_a2(x_77522, f_5K08):
    'rFiitZ0_sw7__N0YN53r_J7I'
    while (f_5K08 < len(x_77522)):
        z78_8_z_ = x_77522[f_5K08]
        if (z78_8_z_ == chr((154 + -95))):
            return (None, len(x_77522))
        elif (z78_8_z_ in wt45LpX):
            f_5K08 += (((-15 + 91) + (-118 + 50)) + ((-180 + 96) + (148 + -71)))
        elif (z78_8_z_ in F4K748__):
            'kSYIq0o3mR496oY__jKf94dU_eH6a'
            return (z78_8_z_, (f_5K08 + (((-108 + 72) + (-117 + 98)) + ((-40 + 83) + (-52 + 65)))))
        elif (z78_8_z_ == chr((104 + -69))):
            return (x_77522[f_5K08:(f_5K08 + (((48 + -54) + (-102 + 62)) + ((49 + 91) + (-173 + 81))))], min((f_5K08 + (((-27 + -15) + (-12 + 60)) + ((-19 + -71) + (88 + -2)))), len(x_77522)))
        elif (z78_8_z_ == chr(((-15 + 94) + (-105 + 70)))):
            if (((f_5K08 + (((100 + -48) + (-114 + 71)) + ((-83 + 76) + (-7 + 6)))) < len(x_77522)) and (x_77522[(f_5K08 + (((36 + -57) + (138 + -56)) + ((-5 + -89) + (114 + -80))))] == chr(((-24 + 45) + (109 + -66))))):
                return ((chr((90 + -46)) + chr((9 + 55))), (f_5K08 + (((89 + -50) + (15 + 17)) + ((-27 + -2) + (47 + -87)))))
            return (z78_8_z_, (f_5K08 + (((109 + -86) + (119 + -66)) + ((16 + -64) + (-126 + 99)))))
        elif (z78_8_z_ in Yq1jCeV):
            if (((f_5K08 + (((-224 + 93) + (34 + 36)) + ((12 + -30) + (66 + 14)))) < len(x_77522)) and (x_77522[(f_5K08 + (((117 + -61) + (13 + -93)) + ((24 + 38) + (-19 + -18))))] == z78_8_z_)):
                return ((z78_8_z_ + z78_8_z_), (f_5K08 + (((-60 + 64) + (80 + 17)) + ((-205 + 29) + (13 + 64)))))
            s82yB = (bytes(x_77522[f_5K08:], encoding=((chr(117) + chr(116)) + ('' + ('f' + '-8')))),)
            vF0_0 = L9a3_E.tokenize(iter(s82yB).__next__)
            next(vF0_0)
            U975Blt3L = next(vF0_0)
            if (U975Blt3L.type != L9a3_E.STRING):
                raise ValueError(((('' + 'in') + ('val' + 'id')) + ((' ' + 'strin') + ('g: {' + '0}'))).format(U975Blt3L.string))
            return (U975Blt3L.string, (U975Blt3L.end[(((33 + -10) + (68 + -92)) + ((91 + -98) + (95 + -86)))] + f_5K08))
        else:
            Bn34 = f_5K08
            while ((Bn34 < len(x_77522)) and (x_77522[Bn34] not in UYz43)):
                Bn34 += (((66 + -94) + (101 + -23)) + ((-15 + -74) + (-46 + 86)))
            return (x_77522[f_5K08:Bn34], min(Bn34, len(x_77522)))
    return (None, len(x_77522))

def tDd9(x_77522):
    'LL4pT_z8N6e88160C_wiJ_A7s_'
    bq9X9 = []
    (U09s36, VE28Mj) = t5_z_a2(x_77522, int(((-0.1753150566142525 + 0.7605135490942644) * 0)))
    while (U09s36 is not None):
        if (U09s36 in x_ki):
            bq9X9.append(U09s36)
        elif ((U09s36 == ('' + (str() + ('' + '#t')))) or (U09s36.lower() == ((str() + ('tr' + 'u')) + 'e'))):
            bq9X9.append(True)
        elif ((U09s36 == (chr(35) + chr((42 + 60)))) or (U09s36.lower() == ((str() + ('' + 'fals')) + chr((155 + -54))))):
            bq9X9.append(False)
        elif (U09s36 == (('n' + chr(105)) + 'l')):
            bq9X9.append(U09s36)
        elif (U09s36[int((((-1.0649654134259947 + 0.9769880981612459) + (-0.33744226032350244 + 0.8615135648673372)) * int(((0.17465290383839305 + 0.7143322430773283) * int((0.6484719932379813 * 0))))))] in C3f8S3c):
            V_1a_Z = False
            if (U09s36[int(((-0.03215048535751919 + 0.4973145249739014) * int((0.00498630224875285 * 0))))] in It1__S71):
                try:
                    bq9X9.append(int(U09s36))
                    V_1a_Z = True
                except ValueError:
                    try:
                        bq9X9.append(float(U09s36))
                        V_1a_Z = True
                    except ValueError:
                        pass
            if (not V_1a_Z):
                if xXk6F(U09s36):
                    bq9X9.append(U09s36.lower())
                else:
                    raise ValueError(((('in' + 'v') + ('alid n' + 'umeral or s')) + (('ym' + 'bo') + ('l: {' + '0}'))).format(U09s36))
        elif (U09s36[int(((-0.08349737342797792 + 0.6162629699191348) * int((0.7990834123701285 * 0))))] in Yq1jCeV):
            bq9X9.append(U09s36)
        else:
            l_995_ = [((str() + ('warning: i' + 'nvalid token:')) + ((' ' + '{') + ('' + '0}'))).format(U09s36), ((chr(((1 + -25) + (-33 + 89))) * (((15 + -81) + (-30 + 81)) + ((40 + -28) + (-15 + 22)))) + x_77522), ((chr(((-61 + 30) + (60 + 3))) * (VE28Mj + (((-19 + -78) + (-89 + 93)) + ((51 + -9) + (118 + -63))))) + chr(((15 + 85) + (-39 + 33))))]
            raise ValueError(chr(((-80 + 100) + (70 + -80))).join(l_995_))
        (U09s36, VE28Mj) = t5_z_a2(x_77522, VE28Mj)
    return bq9X9

def f5_v2S(ZQ_62):
    'sas__PR05P7qO85Tf8__n1_57'
    return (tDd9(x_77522) for x_77522 in ZQ_62)

def v1Hl1H(ZQ_62):
    't25BNGw1d8KA7h_JK_8t4o'
    return len(list(n6f6_r8b_.chain(*f5_v2S(ZQ_62))))

def V94_(*EB1Tdm75):
    import argparse as a82n1_4
    Y_I3G_G9 = a82n1_4.ArgumentParser(description=(str() + (('Count Scheme' + ' toke') + ('ns' + '.'))))
    Y_I3G_G9.add_argument(('f' + (str() + ('i' + 'le'))), nargs='?', type=a82n1_4.FileType(chr(((139 + -39) + (5 + 9)))), default=L5948Fbo.stdin, help=((chr(105) + ('nput' + ' file to be cou')) + (str() + ('nte' + 'd'))))
    EB1Tdm75 = Y_I3G_G9.parse_args()
    print((('c' + ('' + 'ou')) + (('n' + 't') + ('' + 'ed'))), v1Hl1H(EB1Tdm75.file), ('' + (('t' + 'oke') + ('' + 'ns'))))
'Ge591___14Y2Rw_K2_651463_'
__version__ = (str() + (('' + '1.2') + ('.' + '4')))
enIzy308_.DOTS_ARE_CONS = False
enIzy308_.TK_TURTLE = False
enIzy308_.TURTLE_SAVE_PATH = None

def I9pk_7(G8y_e40, kd8FDNX, x_x07=None):
    'n68Ie0k2S8_33X1rCZ275R3_2'
    kd8FDNX.stack.append(G8y_e40)
    if T10r_5F_(G8y_e40):
        bq9X9 = kd8FDNX.jJ4x_(G8y_e40)
        kd8FDNX.stack.pop()
        return bq9X9
    elif hz84n_(G8y_e40):
        kd8FDNX.stack.pop()
        return G8y_e40
    if (not Gm_Xir(G8y_e40)):
        raise s600(((('mal' + 'for') + ('med l' + 'ist: ')) + (str() + ('' + '{0}'))).format(repl_str(G8y_e40)))
    (Wai2, H7dNr_) = (G8y_e40.Wai2, G8y_e40.H7dNr_)
    if (T10r_5F_(Wai2) and (Wai2 in cn88J)):
        bq9X9 = cn88J[Wai2](H7dNr_, kd8FDNX)
        kd8FDNX.stack.pop()
        return bq9X9
    else:
        Qt6_a = I9pk_7(Wai2, kd8FDNX)
        H_7_31_(Qt6_a)
        if isinstance(Qt6_a, M5_S_):
            G8y_e40 = Qt6_a.SZS1e6(H7dNr_, kd8FDNX)
            bq9X9 = I9pk_7(G8y_e40, kd8FDNX)
        else:
            EB1Tdm75 = H7dNr_.map((lambda k9da8N_u: I9pk_7(k9da8N_u, kd8FDNX)))
            bq9X9 = g8f33(Qt6_a, EB1Tdm75, kd8FDNX)
        kd8FDNX.stack.pop()
        return bq9X9

def hz84n_(G8y_e40):
    'F_R75_trp21l_3_R_00_SVk'
    return ((ltJ2(G8y_e40) and (not T10r_5F_(G8y_e40))) or (G8y_e40 is None))

def g8f33(Qt6_a, EB1Tdm75, kd8FDNX):
    'T_15y8B81Z_E9_471X_1A86NW5_pA'
    if isinstance(Qt6_a, BuiltinProcedure):
        return Qt6_a.mY1u(EB1Tdm75, kd8FDNX)
    else:
        p3_9mu_ = Qt6_a.AqoF6(EB1Tdm75, kd8FDNX)
        return Wf_1Ij09(Qt6_a.i_8__, p3_9mu_)

def Wf_1Ij09(D_5sA5_67, kd8FDNX):
    'Z020mKvtYQ798MjZywGI__51q'
    dFN562aq = None
    while (D_5sA5_67 is not nil):
        SF78250 = (D_5sA5_67.H7dNr_ is nil)
        dFN562aq = I9pk_7(D_5sA5_67.Wai2, kd8FDNX, SF78250)
        D_5sA5_67 = D_5sA5_67.H7dNr_
    return dFN562aq

class Fd2t(object):
    'ur4xjp0_yee4RK_S687_Adj47'

    def __init__(H_9G4L_X, vD_3):
        'TPZ63n54_V52uf9r7Bz0'
        H_9G4L_X.t___534 = {}
        H_9G4L_X.vD_3 = vD_3
        if H_9G4L_X.vD_3:
            H_9G4L_X.stack = H_9G4L_X.vD_3.stack
        else:
            H_9G4L_X.stack = []

    def __repr__(H_9G4L_X):
        if (H_9G4L_X.vD_3 is None):
            return ((('' + '<G') + ('' + 'lobal Fra')) + ('' + ('' + 'me>')))
        P_7q887A_ = sorted([((('{' + '0') + '}') + (('' + ': ') + ('{' + '1}'))).format(f_5K08, q5Y3900g) for (f_5K08, q5Y3900g) in H_9G4L_X.t___534.items()])
        return ((('' + '<{{{') + ('0}}} ' + '-')) + (('> ' + '{') + ('1' + '}>'))).format((str() + (str() + (',' + ' '))).join(P_7q887A_), repr(H_9G4L_X.vD_3))

    def y__2L3Z3(H_9G4L_X, N__f5_3Y, dFN562aq):
        'cTp341sE1i7lumc_a46z3SX3_'
        H_9G4L_X.t___534[N__f5_3Y] = dFN562aq

    def jJ4x_(H_9G4L_X, N__f5_3Y):
        'CUTL6Z3b3_2Y_LJ8_86E08IT_'
        K_2f5Wj__ = H_9G4L_X
        while (K_2f5Wj__ is not None):
            if (N__f5_3Y in K_2f5Wj__.t___534):
                return K_2f5Wj__.t___534[N__f5_3Y]
            K_2f5Wj__ = K_2f5Wj__.vD_3
        raise s600(((('unknown identifi' + 'er:') + ' ') + (('{' + '0') + '}')).format(N__f5_3Y))

    def u9__w(H_9G4L_X, N__f5_3Y, dFN562aq):
        'Gxc3_Wur6aQ3_h_8i7To'
        K_2f5Wj__ = H_9G4L_X
        while (K_2f5Wj__ is not None):
            if (N__f5_3Y in K_2f5Wj__.t___534):
                K_2f5Wj__.t___534[N__f5_3Y] = dFN562aq
                return
            K_2f5Wj__ = K_2f5Wj__.vD_3
        raise s600(((str() + ('unknown identifi' + 'er: {')) + (chr(48) + '}')).format(N__f5_3Y))

    def dka935a7(H_9G4L_X, A1fY771w, BFq2H8q):
        'P73qXO_cs9DGEBK___e_'
        if (len(A1fY771w) != len(BFq2H8q)):
            raise s600(((('Incorrect num' + 'ber of arguments t') + ('' + 'o fun')) + (('ction' + ' ca') + ('l' + 'l'))))
        cq95 = Fd2t(H_9G4L_X)
        while isinstance(A1fY771w, Pair):
            if A_3b18(A1fY771w.Wai2):
                assert (A1fY771w.H7dNr_ is nil), ((('sh' + 'ould have been caught earl') + ('' + 'ie')) + chr((167 + -53)))
                cq95.y__2L3Z3(P_7tpp45(A1fY771w.Wai2), BFq2H8q)
                return cq95
            cq95.y__2L3Z3(A1fY771w.Wai2, BFq2H8q.Wai2)
            (A1fY771w, BFq2H8q) = (A1fY771w.H7dNr_, BFq2H8q.H7dNr_)
        if (A1fY771w != nil):
            cq95.y__2L3Z3(A1fY771w, BFq2H8q)
        elif (BFq2H8q != nil):
            raise s600(((('too' + ' man') + ('y ' + 'a')) + (('rguments to f' + 'unction') + (' ca' + 'll'))))
        return cq95

class CME266t_(object):
    'M_BZ_y_Ns0GI___9787_4x'

def j5Dn81OD(rPt_ajbd):
    return isinstance(rPt_ajbd, CME266t_)

class BuiltinProcedure(CME266t_):
    'w7p5YiH7joTKXX_Is266'

    def __init__(H_9G4L_X, r2__13, Ms_68_12R=False, f__cU0_='builtin'):
        H_9G4L_X.f__cU0_ = f__cU0_
        H_9G4L_X.r2__13 = r2__13
        H_9G4L_X.Ms_68_12R = Ms_68_12R

    def __str__(H_9G4L_X):
        return (('' + ('' + '#[')) + (('{' + '0}') + ']')).format(H_9G4L_X.f__cU0_)

    def mY1u(H_9G4L_X, EB1Tdm75, kd8FDNX):
        'vpb4_6mSlsG2v_2V5_g19xU4Gm'
        if (not Gm_Xir(EB1Tdm75)):
            raise s600(((('' + 'arguments ar') + ('e not in a lis' + 't: {0')) + '}').format(EB1Tdm75))
        V3Sw = []
        while (EB1Tdm75 is not nil):
            V3Sw.append(EB1Tdm75.Wai2)
            EB1Tdm75 = EB1Tdm75.H7dNr_
        if H_9G4L_X.Ms_68_12R:
            V3Sw.append(kd8FDNX)
        try:
            return H_9G4L_X.r2__13(*V3Sw)
        except TypeError as b7rvKk__:
            raise s600(((('incorr' + 'ect number') + (' o' + 'f argum')) + (('ent' + 's') + ('' + ': {0}'))).format(H_9G4L_X))

class LambdaProcedure(CME266t_):
    'OFp__x2u__R23_73J2_r'
    f__cU0_ = ((chr(91) + chr(108)) + ('a' + ('mbda' + ']')))

    def __init__(H_9G4L_X, A1fY771w, i_8__, kd8FDNX):
        'klJ7U2e54_0rI2a16_YU61n24'
        assert isinstance(kd8FDNX, Fd2t), ((('e' + 'n') + ('' + 'v must be of t')) + (str() + ('ype F' + 'rame')))
        K96a7_3X(A1fY771w, Gm_Xir, 0, ((('' + 'La') + ('mb' + 'da')) + (('' + 'Pro') + ('cedu' + 're'))))
        K96a7_3X(i_8__, Gm_Xir, (((-40 + -73) + (150 + -70)) + ((206 + -79) + (-48 + -45))), ((('La' + 'mbdaProce') + ('d' + 'u')) + (chr(114) + chr(101))))
        H_9G4L_X.A1fY771w = A1fY771w
        H_9G4L_X.i_8__ = i_8__
        H_9G4L_X.kd8FDNX = kd8FDNX

    def AqoF6(H_9G4L_X, EB1Tdm75, kd8FDNX):
        'fc_6O8_4M_9O8_X4bs3_06'
        return H_9G4L_X.kd8FDNX.dka935a7(H_9G4L_X.A1fY771w, EB1Tdm75)

    def __str__(H_9G4L_X):
        return str(Pair((('l' + ('a' + 'm')) + ('b' + ('' + 'da'))), Pair(H_9G4L_X.A1fY771w, H_9G4L_X.i_8__)))

    def __repr__(H_9G4L_X):
        return ((('LambdaProcedure({0' + '}, {1},') + ('' + ' {')) + ('' + ('2}' + ')'))).format(repr(H_9G4L_X.A1fY771w), repr(H_9G4L_X.i_8__), repr(H_9G4L_X.kd8FDNX))

class M5_S_(LambdaProcedure):
    'E5K0Nm26825O_lMY__6ix945_'

    def SZS1e6(H_9G4L_X, UHq__I_CE, kd8FDNX):
        'Lx_861w_Z5t4x5W_7713i8_0xqBq4'
        return b5_9U_9(H_9G4L_X, UHq__I_CE, kd8FDNX)

def ODx_t(henX44, hx4r___8_):
    'm2105Ftf5P9384I7497V'
    for (f__cU0_, r2__13, c469Gk3E) in hx4r___8_:
        henX44.y__2L3Z3(f__cU0_, BuiltinProcedure(r2__13, f__cU0_=c469Gk3E))

def NA4C(D_5sA5_67, kd8FDNX):
    'Y_8032_1_Fq_94_7GG84E4c93I'
    F_AGJ2DUn(D_5sA5_67, (((-105 + 47) + (37 + -33)) + ((7 + -27) + (159 + -83))))
    m4b4 = D_5sA5_67.Wai2
    if T10r_5F_(m4b4):
        F_AGJ2DUn(D_5sA5_67, (((78 + -22) + (-15 + 30)) + ((-52 + -5) + (48 + -60))), (((114 + -94) + (-23 + 94)) + ((-23 + -79) + (-65 + 78))))
        dFN562aq = I9pk_7(D_5sA5_67.H7dNr_.Wai2, kd8FDNX)
        kd8FDNX.y__2L3Z3(m4b4, dFN562aq)
        return m4b4
    elif (isinstance(m4b4, Pair) and T10r_5F_(m4b4.Wai2)):
        f__cU0_ = m4b4.Wai2
        A1fY771w = m4b4.H7dNr_
        i_8__ = D_5sA5_67.H7dNr_
        dFN562aq = X8X5vZ21_(Pair(A1fY771w, i_8__), kd8FDNX)
        dFN562aq.f__cU0_ = f__cU0_
        kd8FDNX.y__2L3Z3(f__cU0_, dFN562aq)
        return f__cU0_
    else:
        ei67_ = (m4b4.Wai2 if isinstance(m4b4, Pair) else m4b4)
        raise s600(((('no' + 'n-s') + ('ymbo' + 'l:')) + ((' ' + '{') + ('' + '0}'))).format(ei67_))

def nL9_(D_5sA5_67, kd8FDNX):
    'am727uc5yULE_yj4u_2h3L_9_74wD'
    F_AGJ2DUn(D_5sA5_67, (((-26 + 82) + (120 + -84)) + ((10 + -18) + (11 + -94))), (((8 + -18) + (-64 + 75)) + int(((0.25218619657207764 + 0.5146327297820761) * int((0.2605534525384592 * 0))))))
    return D_5sA5_67.Wai2

def hL23__(D_5sA5_67, kd8FDNX):
    'R7_h2N_3_6s4WX4F__8x7D_'
    F_AGJ2DUn(D_5sA5_67, (((63 + -33) + (-3 + 31)) + ((-49 + 57) + (-107 + 42))))
    return Wf_1Ij09(D_5sA5_67, kd8FDNX)

def X8X5vZ21_(D_5sA5_67, kd8FDNX):
    'l0AA9_I_Wf41Gm_50B27T3_6O'
    F_AGJ2DUn(D_5sA5_67, (((104 + -98) + (-108 + 19)) + ((226 + -88) + (-16 + -37))))
    A1fY771w = D_5sA5_67.Wai2
    aIzq_(A1fY771w)
    return LambdaProcedure(A1fY771w, D_5sA5_67.H7dNr_, kd8FDNX)

def c8_86mZ7(D_5sA5_67, kd8FDNX):
    'WL9hv75j75vw31__whA_f_t'
    F_AGJ2DUn(D_5sA5_67, (((55 + -18) + (22 + -35)) + ((-9 + 76) + (-34 + -55))), (((188 + -59) + (-111 + 21)) + ((70 + -47) + (-19 + -40))))
    if J3Zs5b(I9pk_7(D_5sA5_67.Wai2, kd8FDNX)):
        return I9pk_7(D_5sA5_67.H7dNr_.Wai2, kd8FDNX, True)
    elif (len(D_5sA5_67) == (((-122 + -31) + (43 + 43)) + ((39 + -6) + (-51 + 88)))):
        return I9pk_7(D_5sA5_67.H7dNr_.H7dNr_.Wai2, kd8FDNX, True)

def ZrelW(D_5sA5_67, kd8FDNX):
    'R7__f9QaG_99z_8g7862QF'
    dFN562aq = True
    while (D_5sA5_67 is not nil):
        SF78250 = (D_5sA5_67.H7dNr_ is nil)
        dFN562aq = I9pk_7(D_5sA5_67.Wai2, kd8FDNX, SF78250)
        if m__28M6z4(dFN562aq):
            return dFN562aq
        D_5sA5_67 = D_5sA5_67.H7dNr_
    return dFN562aq

def x_6j__6V0(D_5sA5_67, kd8FDNX):
    'H_1spr_7k2o1c0F_c0_Xu'
    dFN562aq = False
    while (D_5sA5_67 is not nil):
        SF78250 = (D_5sA5_67.H7dNr_ is nil)
        dFN562aq = I9pk_7(D_5sA5_67.Wai2, kd8FDNX, SF78250)
        if J3Zs5b(dFN562aq):
            return dFN562aq
        D_5sA5_67 = D_5sA5_67.H7dNr_
    return dFN562aq

def N03v36(D_5sA5_67, kd8FDNX):
    'L9Mg9qW_ss_j5hKW3B5_o'
    while (D_5sA5_67 is not nil):
        z928 = D_5sA5_67.Wai2
        F_AGJ2DUn(z928, (((-159 + 28) + (11 + 73)) + ((179 + -87) + (-95 + 51))))
        if (z928.Wai2 == (str() + ('e' + ('' + 'lse')))):
            T7LpLv = True
            if (D_5sA5_67.H7dNr_ != nil):
                raise s600(((('else mu' + 'st b') + ('e' + ' ')) + (('' + 'la') + ('s' + 't'))))
        else:
            T7LpLv = I9pk_7(z928.Wai2, kd8FDNX)
        if J3Zs5b(T7LpLv):
            if (len(z928) == (((95 + -23) + (-157 + 98)) + ((60 + -36) + (-77 + 41)))):
                return T7LpLv
            else:
                return Wf_1Ij09(z928.H7dNr_, kd8FDNX)
        D_5sA5_67 = D_5sA5_67.H7dNr_

def T9_hU__(D_5sA5_67, kd8FDNX):
    'Em4o_1_50u3_9X_6_riW__8__98'
    F_AGJ2DUn(D_5sA5_67, (((93 + -92) + (-71 + 60)) + ((65 + 33) + (-144 + 58))))
    noW76 = kgruRJ(D_5sA5_67.Wai2, kd8FDNX)
    return Wf_1Ij09(D_5sA5_67.H7dNr_, noW76)

def kgruRJ(t___534, kd8FDNX):
    'aq5_X27_F16JY19_48_J91q9_N__W'
    if (not Gm_Xir(t___534)):
        raise s600((chr((168 + -70)) + (('' + 'ad b') + ('indings list ' + 'in let form'))))
    (C1qZ_Px06, DTc7782) = (nil, nil)
    while (t___534 is not nil):
        N4210h69_ = t___534.Wai2
        F_AGJ2DUn(N4210h69_, (((135 + -72) + (-55 + 18)) + ((24 + -85) + (-32 + 69))), (((46 + 43) + (-8 + -61)) + ((-2 + -30) + (-48 + 62))))
        f__cU0_ = N4210h69_.Wai2
        vUx_63E = I9pk_7(N4210h69_.H7dNr_.Wai2, kd8FDNX)
        C1qZ_Px06 = Pair(f__cU0_, C1qZ_Px06)
        DTc7782 = Pair(vUx_63E, DTc7782)
        t___534 = t___534.H7dNr_
    aIzq_(C1qZ_Px06)
    return kd8FDNX.dka935a7(C1qZ_Px06, DTc7782)

def s6l_267(D_5sA5_67, kd8FDNX):
    't2T423_0_94P23V43j41nt9_2W16'
    F_AGJ2DUn(D_5sA5_67, (((0 + 4) + (146 + -71)) + ((-169 + -7) + (56 + 43))))
    m4b4 = D_5sA5_67.Wai2
    if (isinstance(m4b4, Pair) and T10r_5F_(m4b4.Wai2)):
        f__cU0_ = m4b4.Wai2
        A1fY771w = m4b4.H7dNr_
        i_8__ = D_5sA5_67.H7dNr_
        aIzq_(A1fY771w)
        dFN562aq = M5_S_(A1fY771w, i_8__, kd8FDNX)
        dFN562aq.f__cU0_ = f__cU0_
        kd8FDNX.y__2L3Z3(f__cU0_, dFN562aq)
        return f__cU0_
    else:
        raise s600(((('' + 'improper fo') + ('rm' + ' for d')) + (('efin' + 'e') + ('-mac' + 'ro'))))

def FROeY_5(D_5sA5_67, kd8FDNX):
    'fu33371o73bq0_3z15e83_645c75_'

    def RP__31j3(vUx_63E, kd8FDNX, jg8mE):
        'J_L9x_86q56__LCv___4'
        if (not hmMM9(vUx_63E)):
            return vUx_63E
        if (vUx_63E.Wai2 == (str() + (('u' + 'nq') + ('uo' + 'te')))):
            jg8mE -= (((48 + 2) + (-67 + 78)) + ((-59 + -87) + (184 + -98)))
            if (jg8mE == int((0.5745739367081372 * 0))):
                D_5sA5_67 = vUx_63E.H7dNr_
                F_AGJ2DUn(D_5sA5_67, (((140 + -4) + (30 + -69)) + ((-159 + 39) + (26 + -2))), (((-161 + 97) + (136 + -67)) + ((0 + 32) + (-81 + 45))))
                return I9pk_7(D_5sA5_67.Wai2, kd8FDNX)
        elif (vUx_63E.Wai2 == ('' + (('' + 'qua') + ('siq' + 'uote')))):
            jg8mE += (((15 + 88) + (-76 + 27)) + ((-142 + 71) + (8 + 10)))
        return vUx_63E.map((lambda g16YQ2Dj: RP__31j3(g16YQ2Dj, kd8FDNX, jg8mE)))
    F_AGJ2DUn(D_5sA5_67, (((138 + 0) + (-30 + -57)) + ((-197 + 76) + (33 + 38))), (((-26 + -92) + (76 + -20)) + ((27 + -34) + (102 + -32))))
    return RP__31j3(D_5sA5_67.Wai2, kd8FDNX, (((-39 + 66) + (-128 + 74)) + ((-125 + 89) + (82 + -18))))

def f35Y6(D_5sA5_67, kd8FDNX):
    raise s600(((('unq' + 'uote o') + ('u' + 'tsi')) + (('de of quasiqu' + 'o') + ('t' + 'e'))))

def wGP8t_I(D_5sA5_67, kd8FDNX):
    'Y312VezI77ju8VYr4827t_la'
    F_AGJ2DUn(D_5sA5_67, (((-138 + 78) + (43 + 11)) + ((37 + -14) + (-107 + 92))))
    f__cU0_ = D_5sA5_67.Wai2
    if (not T10r_5F_(f__cU0_)):
        raise s600((((('bad argum' + 'e') + ('nt' + ':')) + chr((42 + -10))) + repl_str(f__cU0_)))
    dFN562aq = I9pk_7(D_5sA5_67.H7dNr_.Wai2, kd8FDNX)
    kd8FDNX.u9__w(f__cU0_, dFN562aq)

def FROeY_5(D_5sA5_67, kd8FDNX):
    'yi8_c4O58z22v63EGv_vW6_c4'
    F_AGJ2DUn(D_5sA5_67, (((112 + -11) + (-145 + 46)) + ((-91 + -2) + (66 + 26))), (((110 + 70) + (-171 + 88)) + ((-238 + 61) + (47 + 34))))

    def RP__31j3(vUx_63E, jg8mE=1):
        'k66U96Dv1Y_72J1__W76233___U14'
        if hmMM9(vUx_63E):
            if (vUx_63E.Wai2 in (((chr(117) + ('' + 'nquot')) + chr((71 + 30))), ((str() + ('unquote' + '-splici')) + ('' + ('' + 'ng'))))):
                jg8mE -= (((-4 + -13) + (6 + -75)) + ((181 + -86) + (-31 + 23)))
                if (jg8mE == int((0.9780266721560428 * 0))):
                    D_5sA5_67 = vUx_63E.H7dNr_
                    F_AGJ2DUn(D_5sA5_67, (((-78 + -71) + (114 + -22)) + ((104 + 34) + (-59 + -21))), (((-136 + 95) + (-27 + 47)) + ((77 + -90) + (76 + -41))))
                    dj_56 = I9pk_7(D_5sA5_67.Wai2, kd8FDNX)
                    m49z = (vUx_63E.Wai2 == ((('u' + 'n') + ('quot' + 'e')) + (('-sp' + 'lic') + ('in' + 'g'))))
                    if (m49z and (not Gm_Xir(dj_56))):
                        K01443 = ((('' + 'un') + ('quote-splicing used ' + 'on non-')) + ('' + ('lis' + 't: {0}')))
                        raise s600(K01443.format(dj_56))
                    return (dj_56 if m49z else Pair(dj_56, nil))
            elif (vUx_63E.Wai2 == ((('' + 'qu') + chr(97)) + (('siqu' + 'o') + ('' + 'te')))):
                jg8mE += (((27 + -69) + (51 + -91)) + ((-23 + 96) + (69 + -59)))
            return Pair(vUx_63E.oJ_0((lambda g16YQ2Dj: RP__31j3(g16YQ2Dj, jg8mE))), nil)
        else:
            return Pair(vUx_63E, nil)
    if (hmMM9(D_5sA5_67.Wai2) and (D_5sA5_67.Wai2.Wai2 == ((('unqu' + 'o') + ('te-' + 'spli')) + (chr(99) + ('i' + 'ng'))))):
        K01443 = ((('un' + 'quote-splicing not in ') + ('list te' + 'mp')) + (('la' + 'te') + (': {' + '0}')))
        raise s600(K01443.format(D_5sA5_67.Wai2))
    return RP__31j3(D_5sA5_67.Wai2).Wai2

def qcn0v(D_5sA5_67, kd8FDNX):
    raise s600(((('Can' + 'no') + ('t' + ' ev')) + (chr(97) + ('luate va' + 'riadic symbol'))))
cn88J = {(str() + (('a' + 'n') + chr(100))): ZrelW, (str() + (('' + 'be') + ('' + 'gin'))): hL23__, ((chr(99) + ('' + 'on')) + chr((42 + 58))): N03v36, ((chr(100) + ('e' + 'f')) + ('' + ('' + 'ine'))): NA4C, (str() + (chr(105) + 'f')): c8_86mZ7, ((str() + ('' + 'la')) + (chr(109) + ('bd' + 'a'))): X8X5vZ21_, ('l' + (chr(101) + 't')): T9_hU__, (str() + (chr(111) + chr(114))): x_6j__6V0, ('q' + ('' + ('uo' + 'te'))): nL9_, ((chr(100) + ('e' + 'fin')) + (('e-' + 'm') + ('' + 'acro'))): s6l_267, ('' + (('' + 'qu') + ('asiquo' + 'te'))): FROeY_5, ((('u' + 'nq') + chr(117)) + ('' + ('o' + 'te'))): f35Y6, ((chr(115) + ('e' + 't')) + chr(33)): wGP8t_I, ((('' + 'unquote-splic') + 'i') + ('' + ('' + 'ng'))): f35Y6, ((('v' + 'ar') + ('i' + 'a')) + (str() + ('' + 'dic'))): qcn0v}

def F_AGJ2DUn(G8y_e40, min, max=float('inf')):
    'h__F368f6rRJ_K_52y__M50eZr_'
    if (not Gm_Xir(G8y_e40)):
        raise s600((((('ba' + 'd') + ('ly' + ' form')) + (('e' + 'd') + (' ' + 'expression: '))) + repl_str(G8y_e40)))
    q10N_t49 = len(G8y_e40)
    if (q10N_t49 < min):
        raise s600(((('too few o' + 'per') + ('an' + 'ds')) + ((' in fo' + 'r') + 'm')))
    elif (q10N_t49 > max):
        raise s600((('' + ('to' + 'o ')) + ('m' + ('any' + ' operands in form'))))

def aIzq_(A1fY771w):
    'k34X7_N_40I_j2lV_rZ_OoZ6J_g17'
    c8cv = set()

    def WW6___n(N__f5_3Y, e003HAek):
        if (A_3b18(N__f5_3Y) and e003HAek):
            N__f5_3Y = P_7tpp45(N__f5_3Y)
        if (not T10r_5F_(N__f5_3Y)):
            raise s600(((('non' + '-sy') + ('mbol:' + ' ')) + (chr(123) + ('' + '0}'))).format(N__f5_3Y))
        if (N__f5_3Y in c8cv):
            raise s600(((('duplicate ' + 's') + ('ymbo' + 'l:')) + (chr(32) + ('' + '{0}'))).format(N__f5_3Y))
        c8cv.add(N__f5_3Y)
    while isinstance(A1fY771w, Pair):
        WW6___n(A1fY771w.Wai2, (A1fY771w.H7dNr_ is nil))
        A1fY771w = A1fY771w.H7dNr_
    if (A1fY771w != nil):
        import scheme as dGj2f54_4
        if enIzy308_.DOTS_ARE_CONS:
            WW6___n(A1fY771w, True)
        else:
            raise s600(('' + (('For' + 'mals must be ') + ('a li' + 'st'))))

def H_7_31_(Qt6_a):
    'SY_B_E9HH1D3_50k282__CJZ_'
    if (not j5Dn81OD(Qt6_a)):
        raise s600(((('{0}' + ' is not') + ('' + ' callable')) + ((':' + ' ') + ('' + '{1}'))).format(type(Qt6_a).__name__.lower(), repl_str(Qt6_a)))

class MuProcedure(CME266t_):
    'O7p_3_b03_263_1_3D9hfTN_I'
    f__cU0_ = ((chr(91) + 'm') + (chr(117) + ']'))

    def __init__(H_9G4L_X, A1fY771w, i_8__):
        'b_C4v6rF_V2I6584624G9'
        H_9G4L_X.A1fY771w = A1fY771w
        H_9G4L_X.i_8__ = i_8__

    def AqoF6(H_9G4L_X, EB1Tdm75, kd8FDNX):
        'QU_BKPK0tV4_I30tlQt41mwv_9_'
        return kd8FDNX.dka935a7(H_9G4L_X.A1fY771w, EB1Tdm75)

    def __str__(H_9G4L_X):
        return str(Pair((str() + (str() + ('' + 'mu'))), Pair(H_9G4L_X.A1fY771w, H_9G4L_X.i_8__)))

    def __repr__(H_9G4L_X):
        return ((str() + ('MuP' + 'r')) + (('ocedu' + 'r') + ('e({0}, ' + '{1})'))).format(repr(H_9G4L_X.A1fY771w), repr(H_9G4L_X.i_8__))

def rB_6_25g(D_5sA5_67, kd8FDNX):
    'G1PGt_0789mc_Z1QV1_3'
    F_AGJ2DUn(D_5sA5_67, (((156 + -45) + (-53 + 37)) + ((-97 + -44) + (121 + -73))))
    A1fY771w = D_5sA5_67.Wai2
    aIzq_(A1fY771w)
    return MuProcedure(A1fY771w, D_5sA5_67.H7dNr_)
cn88J[(str() + ('' + ('m' + 'u')))] = rB_6_25g

class Promise(object):
    'D316ln54yXiPf_A0M7_06m_1eX'

    def __init__(H_9G4L_X, F88t_nC, kd8FDNX):
        H_9G4L_X.F88t_nC = F88t_nC
        H_9G4L_X.kd8FDNX = kd8FDNX

    def V_15(H_9G4L_X):
        if (H_9G4L_X.F88t_nC is not None):
            dFN562aq = I9pk_7(H_9G4L_X.F88t_nC, H_9G4L_X.kd8FDNX)
            if ((not enIzy308_.DOTS_ARE_CONS) and (not ((dFN562aq is nil) or isinstance(dFN562aq, Pair)))):
                raise s600((((('result of forcing a pr' + 'omise should ') + ('be a pair or ni' + 'l, but wa')) + (('' + 's ') + ('' + '%s'))) % dFN562aq))
            H_9G4L_X.dFN562aq = dFN562aq
            H_9G4L_X.F88t_nC = None
        return H_9G4L_X.dFN562aq

    def __str__(H_9G4L_X):
        return (('#' + ('[promi' + 'se ({')) + (('0}' + 'forc') + ('' + 'ed)]'))).format(((('n' + chr(111)) + (str() + ('t' + ' '))) if (H_9G4L_X.F88t_nC is not None) else str()))

def fG8k4(D_5sA5_67, kd8FDNX):
    'sN576T52Vu22bU7qf7kE_Ja'
    F_AGJ2DUn(D_5sA5_67, (((-125 + 81) + (91 + -44)) + ((12 + -39) + (77 + -52))), (((127 + -71) + (81 + -97)) + ((-26 + 16) + (61 + -90))))
    return Promise(D_5sA5_67.Wai2, kd8FDNX)

def wxW3CQ22_(D_5sA5_67, kd8FDNX):
    'n7kf7gmRML1Ikc0OEY_7_s10'
    F_AGJ2DUn(D_5sA5_67, (((154 + -35) + (-46 + -22)) + ((-88 + 92) + (-127 + 74))), (((109 + 29) + (-54 + 5)) + ((-88 + -28) + (108 + -79))))
    return Pair(I9pk_7(D_5sA5_67.Wai2, kd8FDNX), fG8k4(D_5sA5_67.H7dNr_, kd8FDNX))
cn88J[((('' + 'cons-s') + ('t' + 'r')) + (('e' + 'a') + 'm'))] = wxW3CQ22_
cn88J[((('' + 'de') + ('' + 'la')) + chr((28 + 93)))] = fG8k4

class G6Go3_(object):
    'eq4xc_TN0l5id29E5Bu_Kc12O_X'

    def __init__(H_9G4L_X, G8y_e40, kd8FDNX):
        H_9G4L_X.G8y_e40 = G8y_e40
        H_9G4L_X.kd8FDNX = kd8FDNX

def b5_9U_9(Qt6_a, EB1Tdm75, kd8FDNX):
    'sn5d7a_vr55437x2XIe48gi'
    H_7_31_(Qt6_a)
    vUx_63E = g8f33(Qt6_a, EB1Tdm75, kd8FDNX)
    if isinstance(vUx_63E, G6Go3_):
        return I9pk_7(vUx_63E.G8y_e40, vUx_63E.kd8FDNX)
    else:
        return vUx_63E

def z18P6_NC8(UZ2oW0T_A):
    'Gp_k_yy8410d_2n265a_bd__8q'

    def hq59tDx8D(G8y_e40, kd8FDNX, SF78250=False):
        'r9bZ25IAn62_3NLJ21425k3t52_'
        if (SF78250 and (not T10r_5F_(G8y_e40)) and (not hz84n_(G8y_e40))):
            return G6Go3_(G8y_e40, kd8FDNX)
        bq9X9 = G6Go3_(G8y_e40, kd8FDNX)
        while isinstance(bq9X9, G6Go3_):
            (G8y_e40, kd8FDNX) = (bq9X9.G8y_e40, bq9X9.kd8FDNX)
            bq9X9 = UZ2oW0T_A(G8y_e40, kd8FDNX)
        return bq9X9
    return hq59tDx8D
if (((('do' + 'c') + ('' + 'tes')) + chr((203 + -87))) not in L5948Fbo.argv[int(((0.674030939345798 + 0.1889126616372786) * int((0.7526663368842963 * 0))))]):
    I9pk_7 = z18P6_NC8(I9pk_7)

def Q4140_6(r2__13, P_7q887A_, kd8FDNX):
    K96a7_3X(r2__13, j5Dn81OD, int((0.490285570105211 * 0)), ((str() + ('m' + 'a')) + chr(112)))
    K96a7_3X(P_7q887A_, Gm_Xir, (((-89 + -44) + (93 + 1)) + ((58 + -92) + (159 + -85))), (str() + (('m' + 'a') + 'p')))
    return P_7q887A_.map((lambda rPt_ajbd: b5_9U_9(r2__13, Pair(rPt_ajbd, nil), kd8FDNX)))

def WO4_7628G(r2__13, P_7q887A_, kd8FDNX):
    K96a7_3X(r2__13, j5Dn81OD, int((((-1.3545132020282031 + 0.7115637821459648) + (0.06566621255606708 + 0.6320634086997606)) * int(((-0.07171057983559126 + 0.5557287520212275) * 0)))), ((str() + ('f' + 'ilt')) + (chr(101) + chr(114))))
    K96a7_3X(P_7q887A_, Gm_Xir, (((-135 + 70) + (-17 + 73)) + ((42 + -94) + (152 + -90))), ((('' + 'fi') + ('' + 'lte')) + chr((34 + 80))))
    (fY3QW0_, current) = (nil, nil)
    while (P_7q887A_ is not nil):
        (J2M3, P_7q887A_) = (P_7q887A_.Wai2, P_7q887A_.H7dNr_)
        if b5_9U_9(r2__13, Pair(J2M3, nil), kd8FDNX):
            if (fY3QW0_ is nil):
                fY3QW0_ = Pair(J2M3, nil)
                current = fY3QW0_
            else:
                current.H7dNr_ = Pair(J2M3, nil)
                current = current.H7dNr_
    return fY3QW0_

def a3m_4m_37(r2__13, P_7q887A_, kd8FDNX):
    K96a7_3X(r2__13, j5Dn81OD, int((((-0.6206289395855948 + 0.3639691581043847) + (-0.004729262243703958 + 0.33075586612112395)) * int((0.9888267212074857 * 0)))), ((('' + 'red') + ('' + 'uc')) + chr((20 + 81))))
    K96a7_3X(P_7q887A_, (lambda rPt_ajbd: (rPt_ajbd is not nil)), (((102 + -9) + (-15 + -15)) + ((-70 + -84) + (77 + 15))), ((chr(114) + ('e' + 'du')) + (chr(99) + chr(101))))
    K96a7_3X(P_7q887A_, Gm_Xir, (((47 + -69) + (-60 + 11)) + ((84 + 50) + (-8 + -54))), ((('' + 're') + ('d' + 'u')) + (chr(99) + chr(101))))
    (dFN562aq, P_7q887A_) = (P_7q887A_.Wai2, P_7q887A_.H7dNr_)
    while (P_7q887A_ is not nil):
        dFN562aq = b5_9U_9(r2__13, md3tap9m(dFN562aq, P_7q887A_.Wai2), kd8FDNX)
        P_7q887A_ = P_7q887A_.H7dNr_
    return dFN562aq

def Y7G_(Ud0948, kd8FDNX, o172=False, U44x2=False, Q114XRG_=False, O_09R8=(), hB97uMMe3=False):
    'G8ya0vU8_v_1_3vc2pV4V7_'
    if Q114XRG_:
        try:
            Uzc_0eB6(((('' + 'sc') + 'h') + (('em' + 'e') + ('' + '_lib'))), True, kd8FDNX)
        except s600:
            pass
        for Y27vn5 in O_09R8:
            Uzc_0eB6(Y27vn5, True, kd8FDNX)
    while True:
        try:
            kSv_H_9aX = Ud0948()
            while kSv_H_9aX.WN0Y_:
                F88t_nC = Zb___69vz(kSv_H_9aX)
                bq9X9 = I9pk_7(F88t_nC, kd8FDNX)
                if ((not U44x2) and (bq9X9 is not None)):
                    print(repl_str(bq9X9))
        except (s600, SyntaxError, ValueError, RuntimeError) as b7rvKk__:
            if hB97uMMe3:
                if isinstance(b7rvKk__, SyntaxError):
                    b7rvKk__ = s600(b7rvKk__)
                    raise b7rvKk__
            hV__(kd8FDNX)
            if (isinstance(b7rvKk__, RuntimeError) and (((chr(109) + ('ax' + 'imum r')) + (('ecursio' + 'n depth exce') + ('ed' + 'ed'))) not in getattr(b7rvKk__, ((str() + ('ar' + 'g')) + 's'))[int(((0.31287314228108487 + 0.45844675138575375) * int((0.6800170816558342 * 0))))])):
                raise
            elif isinstance(b7rvKk__, RuntimeError):
                print(((str() + ('Erro' + 'r: maximum')) + ((' rec' + 'u') + ('rsion de' + 'pth exceeded'))))
            else:
                print(((str() + ('Erro' + 'r')) + chr((43 + 15))), b7rvKk__)
        except KeyboardInterrupt:
            if (not Q114XRG_):
                raise
            kd8FDNX.stack = []
            print()
            print(((('Ke' + 'y') + ('bo' + 'ardIn')) + (('te' + 'r') + ('rup' + 't'))))
            if (not o172):
                return
        except EOFError:
            print()
            return
H__33NWh7 = {((chr(115) + 'e') + 't'): (str() + ('s' + ('et' + '!')))}

def hV__(kd8FDNX):
    print(((chr(84) + ('' + 'raceback (most recent ')) + (('cal' + 'l last') + (')' + ':'))))
    for (Lt__7g521, G8y_e40) in enumerate(kd8FDNX.stack):
        print(((chr((-63 + 95)) + ' ') + str(Lt__7g521)), repl_str(G8y_e40), sep=chr(((-122 + 42) + (91 + -2))))
    kd8FDNX.stack[:] = []

def Uzc_0eB6(*EB1Tdm75):
    'c8___NzUM_dr4_0p768K52_xD'
    if (not ((((-102 + 22) + (-1 + 8)) + ((72 + -81) + (103 + -19))) <= len(EB1Tdm75) <= (((-69 + 9) + (50 + -81)) + ((221 + -37) + (-138 + 48))))):
        D_5sA5_67 = EB1Tdm75[:(- (((-66 + 45) + (58 + 31)) + ((-181 + 83) + (4 + 27))))]
        raise s600(((('"lo' + 'ad') + ('"' + ' ')) + (('given incorre' + 'c') + ('t number of arguments: ' + '{0}'))).format(len(D_5sA5_67)))
    z5x_7G12 = EB1Tdm75[int(((-0.15266406722426928 + 0.9305128320825211) * 0))]
    U44x2 = (EB1Tdm75[(((-59 + 26) + (-50 + 22)) + ((79 + 19) + (-54 + 18)))] if (len(EB1Tdm75) > (((162 + -8) + (-164 + 94)) + ((-279 + 98) + (110 + -11)))) else True)
    kd8FDNX = EB1Tdm75[(- (((20 + -93) + (31 + -45)) + ((62 + 67) + (-123 + 82))))]
    if E_I3(z5x_7G12):
        z5x_7G12 = eval(z5x_7G12)
    K96a7_3X(z5x_7G12, T10r_5F_, int((((-0.5454509449943181 + 0.16397587107951506) + (0.039956113125870885 + 0.6399967635258975)) * int((0.1548128134186587 * 0)))), ('l' + (str() + ('' + 'oad'))))
    with W_92(z5x_7G12) as OYEiv0l:
        C3m_ = OYEiv0l.readlines()
    EB1Tdm75 = ((C3m_, None) if U44x2 else (C3m_,))

    def Ud0948():
        return m_2XuJE(*EB1Tdm75)
    G__4 = kd8FDNX.stack[:]
    kd8FDNX.stack[:] = []
    Y7G_(Ud0948, kd8FDNX, U44x2=U44x2, hB97uMMe3=True)
    kd8FDNX.stack[:] = G__4

def Ff2f1T0U2(N00b4476, kd8FDNX):
    'Q135psl_v5627anIgYiwQ3'
    assert E_I3(N00b4476)
    N00b4476 = eval(N00b4476)
    import os as ml4_86Q72
    for rPt_ajbd in sorted(ml4_86Q72.listdir('.')):
        if (not rPt_ajbd.endswith((('.' + chr(115)) + (str() + ('' + 'cm'))))):
            continue
        Uzc_0eB6(rPt_ajbd, kd8FDNX)

def W_92(Y27vn5):
    'APA1_9_1_17I8kS188_6Un9'
    try:
        return open(Y27vn5)
    except IOError as jh3W_4:
        if Y27vn5.endswith((chr((45 + 1)) + ('s' + ('c' + 'm')))):
            raise s600(str(jh3W_4))
    try:
        return open((Y27vn5 + ((str() + ('.' + 's')) + ('c' + 'm'))))
    except IOError as jh3W_4:
        raise s600(str(jh3W_4))

def EDG_():
    'Sg7j7_jEELy5Dnwj046a9AS_3F__'
    kd8FDNX = Fd2t(None)
    kd8FDNX.y__2L3Z3(('e' + ('v' + ('' + 'al'))), BuiltinProcedure(I9pk_7, True, ((('' + 'ev') + chr(97)) + chr(108))))
    kd8FDNX.y__2L3Z3((chr(97) + (chr(112) + ('' + 'ply'))), BuiltinProcedure(b5_9U_9, True, (('' + ('' + 'ap')) + (('' + 'pl') + chr(121)))))
    kd8FDNX.y__2L3Z3(((chr(108) + chr(111)) + (str() + ('a' + 'd'))), BuiltinProcedure(Uzc_0eB6, True, (('l' + chr(111)) + (str() + ('' + 'ad')))))
    kd8FDNX.y__2L3Z3(((('' + 'lo') + ('a' + 'd-')) + ('' + ('al' + 'l'))), BuiltinProcedure(Ff2f1T0U2, True, (str() + (('l' + 'oa') + ('d-al' + 'l')))))
    kd8FDNX.y__2L3Z3(((('' + 'pro') + 'c') + (('ed' + 'ur') + ('' + 'e?'))), BuiltinProcedure(j5Dn81OD, False, ((('' + 'pr') + ('oc' + 'edu')) + (('' + 're') + '?'))))
    kd8FDNX.y__2L3Z3((str() + (str() + ('m' + 'ap'))), BuiltinProcedure(Q4140_6, True, (chr((93 + 16)) + ('a' + 'p'))))
    kd8FDNX.y__2L3Z3((str() + ('f' + ('il' + 'ter'))), BuiltinProcedure(WO4_7628G, True, ((chr(102) + 'i') + (('l' + 'te') + 'r'))))
    kd8FDNX.y__2L3Z3((chr((38 + 76)) + ('e' + ('duc' + 'e'))), BuiltinProcedure(a3m_4m_37, True, (('' + ('r' + 'e')) + (('d' + 'u') + ('c' + 'e')))))
    kd8FDNX.y__2L3Z3(((('un' + 'd') + chr(101)) + (('' + 'fin') + ('' + 'ed'))), None)
    kd8FDNX.stack = []
    ODx_t(kd8FDNX, B3tv9)
    return kd8FDNX

def V94_(*argv):
    import argparse as a82n1_4
    Y_I3G_G9 = a82n1_4.ArgumentParser(description=((('' + 'CS 61A S') + ('' + 'ch')) + (('e' + 'm') + ('e Int' + 'erpreter'))))
    import __main__ as bO8_
    if (('' + (str() + ('logi' + 'c'))) in bO8_.__file__):
        F2___6 = ('L' + (('o' + 'g') + ('' + 'ic')))
    else:
        F2___6 = (str() + (('S' + 'che') + ('' + 'me')))
    version = bO8_.__version__
    Y_I3G_G9.add_argument((str() + (('' + '--ve') + ('rs' + 'ion'))), action=((chr(118) + 'e') + ('' + ('rsi' + 'on'))), version=(chr((136 + -13)) + chr((73 + 52))).format(version))
    Y_I3G_G9.add_argument(((('--dots' + '-') + ('ar' + 'e')) + (('-co' + 'n') + 's')), action=((str() + ('' + 'st')) + (chr(111) + ('r' + 'e_true'))), help=((('run with pre-sp19 dotted ' + 'lists behavior where d') + ('' + 'ot')) + (('s are' + ' con') + chr(115))))
    Y_I3G_G9.add_argument(((('' + '--pi') + chr(108)) + (('low-turt' + 'l') + 'e')), action=(str() + (('stor' + 'e_tr') + ('' + 'ue'))), help=((('run with ' + 'pi') + ('llow-based turt' + 'le.')) + ((' This is much faster' + ' for r') + ('endering but there is no ' + 'GUI'))))
    Y_I3G_G9.add_argument(((('--' + 'turt') + ('le-s' + 'ave-p')) + (chr(97) + ('' + 'th'))), default=None, help=((('save the ' + 'im') + ('age t' + 'o thi')) + (('' + 's ') + ('loc' + 'ation when done'))))
    Y_I3G_G9.add_argument((('' + ('-' + 'l')) + (str() + ('oa' + 'd'))), ('-' + chr((14 + 91))), action=((('st' + 'o') + 'r') + (('e' + '_tru') + 'e')), help=((chr(114) + ('u' + 'n')) + ((' file i' + 'ntera') + ('ctive' + 'ly'))))
    Y_I3G_G9.add_argument((str() + (str() + ('fil' + 'e'))), nargs='?', type=a82n1_4.FileType(chr((45 + 69))), default=None, help=(('' + ('S' + 'c')) + (('heme file ' + 'to ') + ('ru' + 'n'))))
    EB1Tdm75 = Y_I3G_G9.parse_args()
    import builtins as enIzy308_
    enIzy308_.DOTS_ARE_CONS = EB1Tdm75.dots_are_cons
    enIzy308_.TK_TURTLE = (not EB1Tdm75.pillow_turtle)
    enIzy308_.TURTLE_SAVE_PATH = EB1Tdm75.turtle_save_path
    L5948Fbo.path.insert(int((((-0.4988250307551356 + 0.024842801437138684) + (0.6221905405624955 + 0.01410305890084318)) * int(((-0.07538883208235259 + 0.9613148138146811) * int((0.389496119473955 * 0)))))), str())
    Ud0948 = kTx61Z_Yr
    o172 = True
    O_09R8 = []
    if (EB1Tdm75.file is not None):
        if EB1Tdm75.load:
            O_09R8.append(getattr(EB1Tdm75.file, ((('' + 'na') + chr(109)) + 'e')))
        else:
            C3m_ = EB1Tdm75.file.readlines()

            def Ud0948():
                return m_2XuJE(C3m_)
            o172 = False
    print(((('Welco' + 'me to the CS 61A {} Interpreter') + (' (v' + 'ersion ')) + (chr(123) + ('}' + ')'))).format(F2___6, version))
    Y7G_(Ud0948, EDG_(), Q114XRG_=True, o172=o172, O_09R8=O_09R8)
    A255ea8()

