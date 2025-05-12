import re
#from summa import summarizer
#from sumy.summarizers.lex_rank import LexRankSummarizer
#from sumy.parsers.plaintext import PlaintextParser
#from sumy.nlp.tokenizers import Tokenizer


def summarize(text):
    LANGUAGE = "english"
    summarizer_lex = LexRankSummarizer()

    parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
    summary= summarizer_lex(parser.document, 2) #Summarize using sumy LexRank
    lex_summary=""
    for sentence in summary:
        lex_summary += str(sentence)
    return lex_summary

def summarize_bad(text):
    return summarizer.summarize(text)

def user_markdown(message):
    div = '<div class="chat-row row-reverse">'
    div += '<img class="chat-icon" src="./app/static/user_icon1.png" width=60 height=60>'
    div += '<div class="chat-bubble human-bubble">'+message+' </div>  </div>'
    return div

def usernoimage_markdown(message):
    div = '<div class="chat-row row-reverse">'
    div += '<div class="chat-bubble human-bubble">'+message+' </div>  </div>'
    return div

def assistant_markdown(message):
    div = '<div class="chat-row">'
#    div += '<img class="chat-icon" src="./app/static/ai_icon1.png" width=40 height=40>'
    div += '<img class="chat-icon" src="./app/static/bot3.png" width=40 height=40>'
    div += '<div class="chat-bubble ai-bubble">'+message+' </div>  </div>'
    return div

def ww_markdown(message):
    div = '<div class="chat-row">'
#    div += '<img class="chat-icon" src="./app/static/ai_icon1.png" width=40 height=40>'
    div += '<img class="chat-icon" src="./app/static/steve.png" width=70 height=70>'
    div += '<div class="chat-bubble ai-bubble">'+message+' </div>  </div>'
    return div

def steve_markdown(message):
    div = '<div class="chat-row">'
#    div += '<img class="chat-icon" src="./app/static/ai_icon1.png" width=40 height=40>'
    div += '<img class="chat-icon" src="./app/static/steve.png" width=75 height=90>'
    div += '<div class="chat-bubble ai-bubble">'+message+' </div>  </div>'
    return div

def hacker_markdown(message):
    div = '<div class="chat-row">'
    div += '<img class="chat-icon" src="./app/static/hacker.png" width=100 height=95>'
    div += '<div class="chat-bubble ai-bubble">'+message+' </div>  </div>'
    return div

def code_markdown(message):
    div = '<div class="chat-row">'
#    div += '<img class="chat-icon" src="./app/static/ai_icon1.png" width=40 height=40>'
    div += '<img class="chat-icon" src="./app/static/bot2.png" width=40 height=40>'
    div += '<div class="chat-bubble ai-bubble">'+message+' </div>  </div>'
    return div

def fix_indentation(code_block):
    lines = code_block.strip().split('\n')
    fixed_lines = []
    for line in lines:
        stripped_line = line.lstrip()
        if stripped_line.startswith('public ') or stripped_line.startswith('private '):
            fixed_lines.append(line)
        elif line.strip() and not line.startswith(' ' * 4):
            fixed_lines.append(' ' * 4 + line)
        else:
            fixed_lines.append(line)
    return '\n'.join(fixed_lines)

def correct_code(input_text):
    pattern = r'(\\begin\{code\}.*?\\end\{code\})'
    def replace_code_blocks(match):
        return fix_indentation(match.group(1))
    
    processed_text = re.sub(pattern, replace_code_blocks, input_text, flags=re.DOTALL)
    return processed_text

def fix_indentation_old(match):
    code_lines = match.group(1).split('\n')
    if code_lines:
        # Calculate the minimum indentation
        min_indent = min(len(line) - len(line.lstrip()) for line in code_lines if line.strip())
        fixed_lines = [line[min_indent:] if line.strip() else line for line in code_lines]
        return '\n'.join(fixed_lines)
    return match.group(1)

# # Find and replace code blocks
# pattern = r'begin\{code\}(.*?)end\{code\}'
# fixed_text = re.sub(pattern, fix_indentation, input_text, flags=re.DOTALL)

def filter_QA(text):
#    pattern = re.compile("name .* is valid", re.flags)
#    pattern.match(text)
#    r1 = re.search(r"^\w+", xx)
    r1 = re.findall(r"Question:.+\n+Answer:.+\n+", text)
    return text

template = """
You are a friendly chatbot assistant that responds in a conversational
manner to users questions. Keep the answers short, unless specifically
asked by the user to elaborate on something.
Question: {question}

Answer:"""


# create the prompt template
context_template = """
Please use the following context to answer questions.
Context: {context}
---
Question: {question}
Answer: Let's think step by step."""




sv_prompt = f"""## INSTRUCTION
I am programming systemverilog functionals, which are used as model for analog circuits in combination with verilog RTL code.
Generate a systemverilog module which satisfies the given Question, using the examples as prototype examples, how these systemverilog models work.

## CONTEXT: systemverilog EXAMPLES

## Example 1, reverse voltae protection and PreRegulator: hy_vddprot_selfbias
module hy_vddprot_selfbias (EVDD, PVDD1, PVDD2, aux_avdd, aux_cpin, aux_vdd, in2p_strt, in2p_strt_osc, taph, tapl, tst_pavdd, vbg_aux, vdiv_aux);
       input EVDD;
       output PVDD1;
       output PVDD2;
       output aux_avdd;
       output aux_cpin;
       output aux_vdd;
       output in2p_strt;
       output in2p_strt_osc;   // p2n ?
       output taph;
       output tapl;
       output tst_pavdd;
       output vbg_aux;
       input vdiv_aux;

   real VBG_AUX = 1.21;
   real VDD_LV = 5.0;

   real r_evdd;
   real r_pvdd1;
   real r_pvdd2;

   real r_aux_avdd;
   real r_aux_cpin;
   real r_aux_vdd;

   real r_vbg_aux;
   real r_vdiv_aux;

   real r_in2p_strt;
   real r_in2p_strt_osc;

   real r_taph;
   real r_tapl;

   real r_vdd1;
   real r_vdd_lv;
   real r_vdd2;

   real r_aux_offset_t;
   real r_aux_offset;

   always @(*) begin
      r_vdd_lv = 0;
      r_vbg_aux = 0;
      r_in2p_strt = 0;
      r_in2p_strt_osc = 0;
      r_taph = 0;
      r_tapl = 0;
      r_vdd2 = 0;
      r_aux_offset = 0;
      if (r_evdd < 0) begin
         r_vdd1 = r_evdd * 1e-3;
      end
      else begin
         r_vdd1 = 0;
         if (r_evdd > 0.7) begin
            r_vdd1 = r_evdd - 0.05;
            r_vdd_lv = r_vdd1 - 0.5;
            if (r_vdd_lv > VDD_LV)
               r_vdd_lv = VDD_LV;
            r_vbg_aux = r_vdd_lv - 0.25;
            if (r_vbg_aux > VBG_AUX)
               r_vbg_aux = VBG_AUX;
            r_in2p_strt = r_vbg_aux / VBG_AUX * -2e-6;
            r_in2p_strt_osc = r_vbg_aux / VBG_AUX * 2e-6;   // p2n ?
            r_vdd2 = r_vdd1 - 0.3;
            r_taph = r_vdd1 * 4 / 20;
            r_tapl = r_vdd1 * 1 / 20;
            r_aux_offset_t = r_vbg_aux - r_vdiv_aux;
            r_aux_offset = (r_aux_offset_t > 1e-4 || r_aux_offset_t < -1e-4) ? r_aux_offset_t : 0.0;
         end
      end
      r_pvdd1 = r_vdd1;
      r_pvdd2 = r_vdd1;
   end

   always begin
      #100;
      if (r_vbg_aux < 0.7) begin
         r_aux_avdd = 0;
         wait (r_vbg_aux >= 0.7);
      end
      else begin
         if (r_aux_avdd + r_aux_offset * r_vdd2 / 50 > r_vdd2)
            r_aux_avdd = r_vdd2;
         else if (r_aux_avdd + r_aux_offset * r_vdd2 / 50 < 1e-5)
            r_aux_avdd = 1e-5;
         else
            r_aux_avdd = r_aux_avdd + r_aux_offset * r_vdd2 / 50;
      end
      r_aux_cpin = r_aux_avdd;
      r_aux_vdd = r_aux_avdd;
   end

   ip_voffset aux_avdd_voff (aux_avdd_int, aux_avdd);
   ip_voffset aux_cpin_voff (aux_cpin_int, aux_cpin);
   ip_voffset aux_vdd_voff (aux_vdd_int, aux_vdd);
   ip_voffset vbg_aux_voff (vbg_aux_int, vbg_aux);

   initial begin
      $xana_sink (EVDD, r_evdd);
      $xana_source (PVDD1, r_pvdd1);
      $xana_source (PVDD2, r_pvdd1);

      $xana_source (aux_avdd_int, r_aux_avdd);
      $xana_source (aux_cpin_int, r_aux_cpin);
      $xana_source (aux_vdd_int, r_aux_vdd);
      $xana_source (vbg_aux_int, r_vbg_aux);

      $xana_source (in2p_strt, r_in2p_strt);
      $xana_source (in2p_strt_osc, r_in2p_strt_osc);

      $xana_source (taph, r_taph);
      $xana_source (tapl, r_tapl);

      $xana_sink (vdiv_aux, r_vdiv_aux);
   end

endmodule


## Example 2: iphln_l13u_w50u
`timescale 1ns/1ns
module iphln_l13u_w50u (cnw, cne, cse, csw, poly, guard);
       inout cne;
       inout cnw;
       inout cse;
       inout csw;
       inout guard;
       inout poly;

   parameter int id = 0;

   import "DPI" pure function real cos (input real rTheta);
   import "DPI" pure function real fabs (input real val);

   const real pi = 3.14159265358979;

   real r_meas_cnw,r_meas_cne,r_meas_cse,r_meas_csw;
   real r_diff_nwse, r_diff_nesw;
   real r_feed_cnw_v,r_feed_cne_v,r_feed_cse_v,r_feed_csw_v;
   real r_feed_cnw_i,r_feed_cne_i,r_feed_cse_i,r_feed_csw_i;

   real r_Bz;
   real r_phi_Bz;
   real r_Bcoil_z;
   real r_Voff_zns, r_Voff_zew;
   real Temperature;
   real r_Sens_z;   // 3.14e-2 V/V(bias) 1/T
   real r_Tk_z;    // -3.52e-3 1/K

   real r_feed_v;
   real r_vgain = 1.0;

   real r_R_plate = 4.7e3;
   real r_RNE_slice = r_R_plate/4;
   real r_RSE_slice = r_R_plate/4;
   real r_RNW_slice = r_R_plate/4;
   real r_RSW_slice = r_R_plate/4;
   real r_Rat_plate;

   assign r_Rat_plate = r_RNE_slice + r_RSE_slice + r_RNW_slice + r_RSW_slice;

   always @(*) begin
      Temperature = cds_globals.Temperature[id];
      r_Sens_z = cds_globals.Sens[id];
      r_Tk_z = cds_globals.Tk[id];
      r_Voff_zns = cds_globals.Voff_ns[id];
      r_Voff_zew = cds_globals.Voff_ew[id];
      r_Bz = cds_globals.Bz[id];
      r_phi_Bz = cds_globals.phi_Bz[id];
      r_Bcoil_z = cds_globals.Bcoil_z[id];
      r_feed_v = fabs(r_feed_cnw_v - r_feed_cse_v) + fabs(r_feed_cne_v - r_feed_csw_v);
      r_vgain = 1.0 + (r_feed_v - 1.5) * 0.06;   // centered on 3v, 6% increase at 5v application - plates see much less
      if (r_vgain < 0)
         r_vgain = 0;
      r_diff_nwse = r_vgain * r_Sens_z*(1+r_Tk_z*(Temperature-27))*(r_feed_csw_i-r_feed_cne_i)*r_Rat_plate*(r_Bz*cos(2*pi/360*r_phi_Bz)+r_Bcoil_z)+r_Voff_zns;
      r_meas_cnw = (r_feed_cne_v + r_feed_csw_v) / 2.0 + r_diff_nwse/2;
      r_meas_cse = (r_feed_cne_v + r_feed_csw_v) / 2.0 - r_diff_nwse/2;
      r_diff_nesw = r_vgain * r_Sens_z*(1+r_Tk_z*(Temperature-27))*(r_feed_cnw_i-r_feed_cse_i)*r_Rat_plate*(r_Bz*cos(2*pi/360*r_phi_Bz)+r_Bcoil_z)+r_Voff_zew;
      r_meas_cne = (r_feed_cnw_v + r_feed_cse_v) / 2.0 + r_diff_nesw/2;
      r_meas_csw = (r_feed_cnw_v + r_feed_cse_v) / 2.0 - r_diff_nesw/2;
   end

   initial begin
      $display ("Hall H(Z) Plate :: ip18ga_hall/iphln_l13u_w50u id %0d at %m", id);

      $xana_source (cne, r_meas_cne, r_RNE_slice,             ,             );
      $xana_source (csw, r_meas_csw, r_RSW_slice,             ,             );
      $xana_source (cnw, r_meas_cnw, r_RNW_slice,             ,             );
      $xana_source (cse, r_meas_cse, r_RSE_slice,             ,             );
      $xana_sink   (cnw,           ,          , r_feed_cnw_v, r_feed_cnw_i);
      $xana_sink   (cse,           ,          , r_feed_cse_v, r_feed_cse_i);
      $xana_sink   (cne,           ,          , r_feed_cne_v, r_feed_cne_i);
      $xana_sink   (csw,           ,          , r_feed_csw_v, r_feed_csw_i);
   end

endmodule



## Example 3 main bandgap: hm_bandgap_main
`timescale 1ns/1ns
module hm_bandgap_main (bgrd, e_n, sgnd, vbg, vbiasn, vbiasp, vdd, vss);
       output logic bgrd;
       input e_n;
       input sgnd;
       output vbg;
       output vbiasn;
       output vbiasp;
       input vdd;
       input vss;

   real VBG = 1.24;
   real VBIASP = 0.99;
   real VBIASN = 0.65;

   realtime VBG_DELAY = 12.0us;

   real r_vdd;
   real r_vbg;
   real r_vbiasp;
   real r_vbiasn;
   real r_vbg_start;
   real r_vbg_delay;

   task automatic bg_delay (input real start, output real delay);
      #(VBG_DELAY) delay = start;
   endtask

   always @(*) fork
      bg_delay (r_vbg_start, r_vbg_delay);
   join_none

   always @(*) begin
      r_vbiasp = 0;
      r_vbiasn = 0;
      r_vbg_start = 0;
      bgrd = 0;
      if (r_vdd > 0.6 && !e_n) begin
         r_vbg_start = r_vdd - 0.2;
         if (r_vdd > VBG + 0.2) begin
            r_vbg_start = VBG;
         end
         if (r_vbg > VBG - 0.01)
            bgrd = 1'b1;
         r_vbiasp = r_vdd - 0.2;
         r_vbiasn = r_vdd - 0.2;
         if (r_vdd > VBIASP + 0.2) begin
            r_vbiasp = VBIASP;
         end
         if (r_vdd > VBIASN + 0.2) begin
            r_vbiasn = VBIASN;
         end
      end
      if (r_vbg_start > r_vbg_delay)
         r_vbg = r_vbg_delay;
      else
         r_vbg = r_vbg_start;
   end

   initial begin
      $xana_sink (vdd, r_vdd);
      $xana_source (vbg, r_vbg);
      $xana_source (vbiasp, r_vbiasp);
      $xana_source (vbiasn, r_vbiasn);
   end

endmodule


## Example 4 Bandgap : ip_bgpnp
`timescale 1ns/1ns
module ip_bgpnp (bgrd, vbiasn, vbiasp, lpow, sgnd, bgrd_n, te, ibiasn, vbg, atbus, vdd, vss);
       output atbus;
       output bgrd;
       output bgrd_n;
       output [3:0] ibiasn;
       input lpow;
       input sgnd;
       input [1:0] te;
       output vbg;
       output vbiasn;
       output vbiasp;
       inout vdd;
       inout vss;

   real VBG = 1.24;
   real VBIASP = 1.65;
   real VBIASN = 0.99;
   real IBIASN = -3e-6;

   realtime VBG_DELAY = 12.0us;

   real r_vdd;
   real r_vbg;
   real r_vbiasp;
   real r_vbiasn;
   real r_ibiasn;
   real r_atbus;
   real r_vbg_start;
   real r_vbg_delay;

   logic bg_rdy;

   task automatic bg_delay (input real start, output real delay);
      #(VBG_DELAY) delay = start;
   endtask

   always @(*) fork
      bg_delay (r_vbg_start, r_vbg_delay);
   join_none

   always @(*) begin
      r_vbiasp = 0;
      r_vbiasn = 0;
      r_ibiasn = 0;
      r_vbg_start = 0;
      r_atbus = 0;
      bg_rdy = 1'b0;
      if (r_vdd > 0.6) begin
         r_vbg_start = r_vdd - 0.2;
         if (r_vdd > VBG + 0.2) begin
            r_vbg_start = VBG;
         end
         if (r_vbg > VBG - 0.01)
            bg_rdy = 1'b1;
         r_vbiasp = r_vdd - 0.2;
         r_vbiasn = r_vdd - 0.2;
         r_ibiasn = (r_vdd - 0.2) / VBIASN * IBIASN;
         if (r_vdd > VBIASP + 0.2) begin
            r_vbiasp = VBIASP;
         end
         if (r_vdd > VBIASN + 0.2) begin
            r_vbiasn = VBIASN;
            r_ibiasn = IBIASN;
         end
         if (te[1])
            r_atbus += r_vbg;
         if (te[0])
            r_atbus += r_ibiasn;
      end
      if (r_vbg_start > r_vbg_delay)
         r_vbg = r_vbg_delay;
      else
         r_vbg = r_vbg_start;
   end

   assign bgrd = (vdd) ? bg_rdy : 1'bx;
   assign bgrd_n = (vdd) ? !bg_rdy : 1'bx;

   initial begin
      $xana_sink (vdd, r_vdd);
      $xana_source (vbg, r_vbg);
      $xana_source (vbiasp, r_vbiasp);
      $xana_source (vbiasn, r_vbiasn);
      $xana_source (ibiasn[0], r_ibiasn);
      $xana_source (ibiasn[1], r_ibiasn);
      $xana_source (ibiasn[2], r_ibiasn);
      $xana_source (ibiasn[3], r_ibiasn);
   end
endmodule

## Example 5, biasing circuit: ip_bias
module ip_bias (ip2n2u, in2p2u, tempprot, en_n, ibiasn, testtemp, UV, vbg, sgnd, atb, testibias, vdd, vss);
       input UV;
       output atb;
       input en_n;
       output [9:0] ip2n2u;
       output [1:0] in2p2u;
       input ibiasn;
       input sgnd;
       output logic tempprot;
       input testibias;
       input testtemp;
       input vbg;
       inout vdd;
       inout vss;

   real r_vdd;
   real r_vbg;
   real r_ibiasn;
   real r_ip2n2u;
   real r_in2p2u;
   real r_atb;
   real r_vrat;

   always @(*) begin
      r_ip2n2u = 0;
      r_in2p2u = 0;
      r_atb = 0;
      tempprot = (vdd) ? 1'b0 : 1'bx;
      if (r_vdd > 1.1 && r_ibiasn < -1.6e-6 && !en_n) begin
         if (r_vdd > 2.1)
            r_vrat = 1.0;
         else
            r_vrat = r_vdd / 2.1;
         r_ip2n2u = r_vbg / 1.124 * 2e-6 * r_vrat;
         r_in2p2u = r_vbg / 1.124 * -2e-6 * r_vrat;
         if (testibias)
            r_atb = r_in2p2u;
         if (!UV) begin
            if (testtemp)
               tempprot = cds_globals.temperature > 80;
            else
               tempprot = cds_globals.temperature > 180;
         end
      end
   end

   initial begin
      $xana_sink (vdd, r_vdd);
      $xana_sink (vbg, r_vbg);
      $xana_sink (ibiasn, r_ibiasn);
   end

    genvar i;

    generate
       for (i=$low(ip2n2u); i<=$high(ip2n2u); i+=1)
          initial $xana_source (ip2n2u[i], r_ip2n2u);
    endgenerate

    generate
       for (i=$low(in2p2u); i<=$high(in2p2u); i+=1)
          initial $xana_source (in2p2u[i], r_in2p2u);
    endgenerate

endmodule


## Example 6 Hall frontend bias: iphfebias
`timescale 1ns/1ns
module iphfebias (force_tc0, ip2n2u_i, ip2n2u_cnst, in2p4u_ctat, in2p4u_ptat, iref_adc, rctat, rptat1, rptat2, sgnd, tc_sens, trimbias, vbg, vdd, vss);
       input force_tc0;
       input ip2n2u_i;
       output [9:0] ip2n2u_cnst;
       output [1:0] in2p4u_ctat;
       output [1:0] in2p4u_ptat;
       output iref_adc;
       inout rctat;
       inout rptat1;
       inout rptat2;
       input sgnd;
       input [1:0] tc_sens;
       input [2:0] trimbias;
       input vbg;
       inout vdd;
       inout vss;

   real r_vdd;
   real r_ip2n2u_i;
   real r_vbg;

   real Rptat;
   real Rctat;

   real r_ip2n2u_cnst;
   real r_in2p4u_ptat;
   real r_in2p4u_ctat;

   real r_iref_adc;

   wire [3:1] sw;
   wire [6:1] trim;

   iphfebiaslog Ilog (.tc_sens(tc_sens), .force_tc0(force_tc0), .sw_tc(sw), .vdd(vdd), .vss(vss));


   real r_v_rptat2;
   real r_i_vbiasp_ptat;
   real r_i_vbiasp_ctat;
   real r_i_ptat;
   real r_i_ctat;

   real r_i_trimptat;
   real r_i_trimctat;
   real r_i_vbiasp_cnst;

   always @(*) begin
      r_v_rptat2 = 0;
      r_i_vbiasp_ptat = 0;
      r_i_vbiasp_ctat = 0;
      r_i_ptat = 0;
      r_i_ctat = 0;
      r_iref_adc = 0;
      r_i_trimptat = 0;
      r_i_trimctat = 0;
      r_i_vbiasp_cnst = 0;
      r_in2p4u_ptat = 0;
      r_in2p4u_ctat = 0;
      r_ip2n2u_cnst = 0;
      if (r_vdd > 0.85 && r_ip2n2u_i > 0.6e-6 && r_ip2n2u_i < 2.6e-6 && r_vbg > 0.7) begin
         r_v_rptat2 = 0.692;
         r_i_vbiasp_ptat = (r_vbg - r_v_rptat2) / Rptat;
         r_i_vbiasp_ctat = r_v_rptat2 / Rctat;
         r_i_ptat = r_i_vbiasp_ptat / 16;
         r_i_ctat = r_i_vbiasp_ctat / 16;
         r_iref_adc = r_i_ptat * 2;
         r_iref_adc += r_i_ctat * 9;
         if (~sw[1])
            r_iref_adc += r_i_ptat * 1;
         else
            r_iref_adc += r_i_ctat * 1;
         if (~sw[2])
            r_iref_adc += r_i_ptat * 2;
         else
            r_iref_adc += r_i_ctat * 2;
         if (~sw[3])
            r_iref_adc += r_i_ptat * 2;
         else
            r_iref_adc += r_i_ctat * 2;
         r_i_trimptat = r_i_ptat * 4 * 4 / (13 + $countones(trim));
         r_in2p4u_ptat = r_i_trimptat * -16/2;
         r_i_vbiasp_cnst = r_i_trimptat * -5;
         r_i_trimctat = r_i_ctat * 4 * 8 / (13 + $countones(trim));
         r_in2p4u_ctat = r_i_trimctat * -16/2;
         r_i_vbiasp_cnst += r_i_trimctat * -3;
         r_ip2n2u_cnst = r_i_vbiasp_cnst / -2;
      end
   end

   initial begin
      $xana_sink (vdd, r_vdd);
      $xana_sink (ip2n2u_i, r_ip2n2u_i);
      $xana_sink (vbg, r_vbg);
      $xana_sink (rptat1, Rptat);
      $xana_sink (rptat2, Rptat);
      $xana_sink (rctat, Rctat);
      $xana_source (iref_adc, r_iref_adc);
   end

    genvar i;

    generate
       for (i=$low(ip2n2u_cnst); i<=$high(ip2n2u_cnst); i+=1)
          initial $xana_source (ip2n2u_cnst[i], r_ip2n2u_cnst);
    endgenerate

    generate
       for (i=$low(in2p4u_ptat); i<=$high(in2p4u_ptat); i+=1)
          initial $xana_source (in2p4u_ptat[i], r_in2p4u_ptat);
    endgenerate

    generate
       for (i=$low(in2p4u_ctat); i<=$high(in2p4u_ctat); i+=1)
          initial $xana_source (in2p4u_ctat[i], r_in2p4u_ctat);
    endgenerate

endmodule

## Example 7 Hall plate reference: iphferes
module iphferes (iauxn, iauxp, idacauxn, idacauxp, idacinn, idacinp, ioutn, ioutp, rctat, rptat1, rptat2, sgnd, vdd, vinn, vinp, vss);
       inout iauxn;
       inout iauxp;
       input idacauxn;
       input idacauxp;
       input idacinn;
       input idacinp;
       inout ioutn;
       inout ioutp;
       inout rctat;
       inout rptat1;
       inout rptat2;
       inout sgnd;
       inout vdd;
       inout vinn;
       inout vinp;
       inout vss;

   real Ra = 4.6968e3;

   real Rptat;
   real Rctat;

   initial begin
      Rptat = Ra * 7;
      Rctat = Ra * 9;
      $xana_source (rptat1, Rptat);
      $xana_source (rptat2, Rptat);
      $xana_source (rctat, Rctat);
   end
endmodule


## hy_vddprot_selfbias
`timescale 1ns/1ns
module hy_vddprot_selfbias (aux_avdd, aux_cpin, aux_vdd, in2p_strt, in2p_strt_osc, PVDD1, PVDD2, vbg_aux, tapl, tst_pavdd, EVDD, vdiv_aux, ip2n_hv, mode, mode_n, ratiometric, uv, vdd_lv);
       input EVDD;
       output PVDD1;
       output PVDD2;
       output aux_avdd;
       output aux_cpin;
       output aux_vdd;
       output in2p_strt;
       output in2p_strt_osc;
       output ip2n_hv;
       input mode;
       input mode_n;
       output ratiometric;
       output tapl;
       output tst_pavdd;
       input uv;
       output vbg_aux;
       output vdd_lv;
       input vdiv_aux;

   real VBG_AUX = 1.21;
   real VDD_LV = 5.0;

   real r_evdd;
   real r_pvdd1;
   real r_pvdd2;

   real r_aux_avdd;
   real r_aux_cpin;
   real r_aux_vdd;

   real r_vbg_aux;
   real r_vdiv_aux;

   real r_in2p_strt;
   real r_in2p_strt_osc;

   real r_ip2n_hv;

   real r_ratiometric;
   real r_tapl;

   real r_vdd1;
   real r_vdd_lv;
   real r_vdd2;

   real r_aux_offset_t;
   real r_aux_offset;

   always @(*) begin
      r_vdd_lv = 0;
      r_vbg_aux = 0;
      r_in2p_strt = 0;
      r_in2p_strt_osc = 0;
      r_ratiometric = 0;
      r_tapl = 0;
      r_vdd2 = 0;
      r_aux_offset = 0;
      if (r_evdd < 0) begin
         r_vdd1 = r_evdd * 1e-3;
      end
      else begin
         r_vdd1 = 0;
         if (r_evdd > 0.7) begin
            r_vdd1 = r_evdd - 0.05;
            r_vdd_lv = r_vdd1 - 0.5;
            if (mode & ~mode_n & ~uv) begin
               if (r_vdd_lv > VDD_LV)
                  r_vdd_lv = VDD_LV;
            end
            else begin
               if (r_vdd_lv > VDD_LV/2)
                  r_vdd_lv = VDD_LV/2;
            end
            r_vbg_aux = r_vdd_lv - 0.25;
            if (r_vbg_aux > VBG_AUX)
               r_vbg_aux = VBG_AUX;
            r_in2p_strt = r_vbg_aux / VBG_AUX * -2e-6;
            r_in2p_strt_osc = r_vbg_aux / VBG_AUX * 2e-6;   // p2n ?
            r_ip2n_hv = (r_vbg_aux / VBG_AUX + r_vdd1 / 19.0) * 3e-6;
            r_vdd2 = r_vdd1 - 0.3;
            r_ratiometric = r_vdd1 * 3 / 13;
            r_tapl = r_vdd1 * 1 / 13;
            r_aux_offset_t = r_vbg_aux - r_vdiv_aux;
            r_aux_offset = (r_aux_offset_t > 1e-4 || r_aux_offset_t < -1e-4) ? r_aux_offset_t : 0.0;
         end
      end
      r_pvdd1 = r_vdd1;
      r_pvdd2 = 0.0;
   end

   always begin
      #100;
      if (r_vbg_aux < 0.7) begin
         r_aux_avdd = 0;
         wait (r_vbg_aux >= 0.7);
      end
      else begin
         if (r_aux_avdd + r_aux_offset * r_vdd2 / 50 > r_vdd2)
            r_aux_avdd = r_vdd2;
         else if (r_aux_avdd + r_aux_offset * r_vdd2 / 50 < 1e-5)
            r_aux_avdd = 1e-5;
         else
            r_aux_avdd = r_aux_avdd + r_aux_offset * r_vdd2 / 50;
      end
      r_aux_cpin = r_aux_avdd;
      r_aux_vdd = r_aux_avdd;
   end

   ip_voffset aux_avdd_voff (aux_avdd_int, aux_avdd);
   ip_voffset aux_cpin_voff (aux_cpin_int, aux_cpin);
   ip_voffset aux_vdd_voff (aux_vdd_int, aux_vdd);
   ip_voffset vbg_aux_voff (vbg_aux_int, vbg_aux);

   initial begin
      $xana_sink (EVDD, r_evdd);
      $xana_source (PVDD1, r_pvdd1);
      $xana_source (PVDD2, r_pvdd1);

      $xana_source (aux_avdd_int, r_aux_avdd);
      $xana_source (aux_cpin_int, r_aux_cpin);
      $xana_source (aux_vdd_int, r_aux_vdd);
      $xana_source (vbg_aux_int, r_vbg_aux);

      $xana_source (in2p_strt, r_in2p_strt);
      $xana_source (in2p_strt_osc, r_in2p_strt_osc);
      $xana_source (ip2n_hv, r_ip2n_hv);

      $xana_source (ratiometric, r_ratiometric);
      $xana_source (tapl, r_tapl);

      $xana_sink (vdiv_aux, r_vdiv_aux);
   end
endmodule


## Example 8: ip_anareg_refsw
module ip_anareg_refsw (bgrdy, out, sel_ratio, vbg, vdd, vratio, vss);
       input bgrdy;
       output out;
       input sel_ratio;
       input vbg;
       inout vdd;
       input vratio;
       inout vss;

   real r_vdd;
   real r_vbg;
   real r_vratio;
   real r_out;

   always @(*) begin
      r_out = 0;
      if (r_vdd > 0.85) begin
         if (sel_ratio & bgrdy)
            r_out = r_vratio;
         else
            r_out = r_vbg;
      end
   end

   initial begin
      $xana_sink (vdd, r_vdd);
      $xana_sink (vbg, r_vbg);
      $xana_sink (vratio, r_vratio);
      $xana_source (out, r_out);
   end
endmodule


## Example 9 voltage resistor divider: ip_anareg_rdiv
module ip_anareg_rdiv (vdd, vss, divh, divl, ref_iddq, set_0, set_1, sgnd, vdiv, vdiv_aux, vref2p00, vref2p56);
       inout vdd;
       inout vss;
       output divh;
       output divl;
       output ref_iddq;
       input set_0;
       input set_1;
       input sgnd;
       output vdiv;
       output vdiv_aux;
       output vref2p00;
       output vref2p56;

   real Ra = 2.5129e3;
   real Ron = 3.0;

   real r_vdd;
   real r_vdiv_aux;
   real r_divh;
   real r_divl;
   real r_vdiv;
   real r_ref_iddq;
   real r_vref2p00;
   real r_vref2p56;

   real R_vdiv_1;
   real R_vdiv_2;
   real R_vdiv_3;
   real R_vdiv_4;
   real R_vdiv;
   real R_divl;
   real R_divh;
   real R_vdiv_aux;
   real R_vdd_1;
   real R_tot;

   always @(*) begin
      R_vdiv_1 = (~set_0) ? Ron : Ra * 1.0;
      R_vdiv_2 = (set_1) ? Ron : R_vdiv_1 + Ra * 1.0;
      R_vdiv_3 = (set_0 & set_1) ? Ron : R_vdiv_2 + Ra * 20.0;
      R_vdiv_4 = R_vdiv_3 + Ra * 5.0;
      R_vdiv = R_vdiv_4 + Ra * 0.5;
      R_divl = R_vdiv + Ra * 2.0;
      R_divh = R_divl + Ra * 1.0;
      R_vdiv_aux = R_divh + Ra * 0.5;
      R_vdd_1 = R_vdiv_aux + Ra * 5.0;
      R_tot = R_vdd_1 + Ra * 14.0;

      r_vdiv_aux = r_vdd * R_vdiv_aux / R_tot;
      r_divh = r_vdd * R_divh / R_tot;
      r_divl = r_vdd * R_divl / R_tot;
      r_vdiv = r_vdd * R_vdiv / R_tot;
   end

   initial begin
      $xana_sink (vdd, r_vdd);
      $xana_source (vdiv_aux, r_vdiv_aux);
      $xana_source (divh, r_divh);
      $xana_source (divl, r_divl);
      $xana_source (vdiv, r_vdiv);
   end
endmodule


## Example 10 Coildriver: ip_coildriver
module ip_coildriver (avdd, coil_a, coil_b, curr_sel, en_n, in2p_2u, output_sat, polarity, vdd5, vss);
       inout avdd;
       output coil_a;
       output coil_b;
       input [3:0] curr_sel;
       input en_n;
       input in2p_2u;
       output logic output_sat;
       input polarity;
       inout vdd5;
       inout vss;

   real R_COIL = 15;

   real r_avdd;
   real r_in2p_2u;
   real r_vdd5;
   real r_v_coil_a;
   real r_i_coil_a;
   real r_R_coil_a;
   real r_v_coil_b;
   real r_i_coil_b;
   real r_R_coil_b;

   real r_ip2n_10u;
   real r_ref_curr;
   real r_fb_curr;

   real ratio = 1024;

   real r_R_coil;
   real r_vd_coil;
   real r_avdd_cont_a;
   real r_v_cont_a;
   real r_i_cont_a;
   real r_avdd_cont_b;
   real r_v_cont_b;
   real r_i_cont_b;

   always @(*) begin
      r_ip2n_10u = 0;
      r_ref_curr = 0;
      r_fb_curr = 0;
      output_sat = 1'b0;
      ratio = 0;
      r_R_coil = 1e9;
      r_vd_coil = 0;
      r_avdd_cont_a = 0;
      r_v_cont_a = 0;
      r_i_cont_a = 0;
      r_avdd_cont_b = 0;
      r_v_cont_b = 0;
      r_i_cont_b = 0;
      if (r_avdd > 1.1 && !en_n) begin
         r_ip2n_10u = r_in2p_2u * -5.0;
         r_ref_curr = r_ip2n_10u;
         r_ref_curr += (curr_sel * r_ip2n_10u);
         ratio = 1024;
         if (r_vdd5 < 4.0)
            ratio = r_vdd5 / 4.0 * 1024;
         r_fb_curr = r_ref_curr * ratio;
         if (r_R_coil_a == R_COIL || r_R_coil_b == R_COIL)
            r_R_coil = 2e8;
         else
            r_R_coil = (r_R_coil_a + r_R_coil_b)/2;
         if (r_R_coil <= 0)
            r_R_coil = 1e8;
         r_vd_coil = r_fb_curr * r_R_coil;
         if (r_vd_coil > r_avdd) begin
            r_vd_coil = r_avdd;
            r_fb_curr = r_vd_coil / r_R_coil;
            output_sat = 1'b1;
         end
         if (polarity) begin
            r_avdd_cont_b = r_avdd;
            r_v_cont_a = -r_vd_coil;
            r_i_cont_b = r_fb_curr / 2;
            r_i_cont_a = r_fb_curr / 2;
         end
         else begin
            r_avdd_cont_a = r_avdd;
            r_v_cont_b = -r_vd_coil;
            r_i_cont_a = -r_fb_curr / 2;
            r_i_cont_b = -r_fb_curr / 2;
         end
      end
   end

   initial begin
      $xana_sink (avdd, r_avdd);
      $xana_sink (in2p_2u, r_in2p_2u);
      $xana_sink (vdd5, r_vdd5);
      
      $xana_source (coil_a, r_avdd_cont_a,               ,);
      $xana_source (coil_a, r_v_cont_a, r_i_cont_a, R_COIL);
      $xana_sink   (coil_a, r_v_coil_a, r_i_coil_a, r_R_coil_a);

      $xana_source (coil_b, r_avdd_cont_b,               ,);
      $xana_source (coil_b, r_v_cont_b, r_i_cont_a, R_COIL);
      $xana_sink   (coil_b, r_v_coil_b, r_i_coil_b, r_R_coil_b);
   end

endmodule


## Example 11 regulator chargepump: ip_anareg_cp
`timescale 1ns/1ns
module ip_anareg_cp (clk, out, v_in, vdd, vss);
       input clk;
       output out;
       input v_in;
       inout vdd;
       inout vss;

       real r_vdd;
       real r_v_in;
       real r_out;

   bit active;

   always @(posedge clk) begin
      active = 1;
      if (r_vdd < 0.85) begin
         r_out = 0.0;
      end
      else begin
         if ((r_v_in * 1.85 - r_out) > 6e-2 || (r_v_in * 1.85 - r_out) < -6e-2)
            r_out = r_out + (r_v_in * 1.85 - r_out) * 0.3678;
         else
            r_out = r_v_in * 1.85;
         if (r_out < 1e-2)
            r_out = 0.0;
      end
   end

   always begin
      #1000;
      if (active)
         active = 0;
      else
         r_out = r_out * 0.95;
   end

   initial begin
      $xana_sink (vdd, r_vdd);
      $xana_sink (v_in, r_v_in);
      $xana_source (out, r_out);
   end
endmodule

## Example 12 voltage regulator OTA: ip_anareg_ota
`timescale 1ns/1ns
module ip_anareg_ota (inn, inp, ip2n2u, out, vdd, vss);
       input inn;
       input inp;
       input ip2n2u;
       output out;
       inout vdd;
       inout vss;

   real r_vdd;
   real r_ip2n2u;
   real r_inp;
   real r_inn;
   real r_out;

   real r_diff_t;
   real r_diff;
   real r_amp;

   real atten = 15;

   always @(r_inp or r_inn or r_vdd or r_ip2n2u) begin
      #1;
      if (((r_inp > r_vdd || r_inp < 0.0) && (r_inn > r_vdd || r_inn < 0.0)) || r_vdd < 0.85 || r_ip2n2u < 0.45e-6 || r_ip2n2u > 3.5e-6) begin
         r_diff = 0.0;
      end
      else begin
         if (r_inp > r_vdd)
            r_diff_t = (r_vdd - r_inn);
         else if  (r_inn > r_vdd)
            r_diff_t = (r_inp - r_vdd);
         else
            r_diff_t = (r_inp - r_inn);
         r_diff = (r_diff_t > 1e-4 || r_diff_t < -1e-4) ? r_diff_t : 0.0;
         if (r_diff > 1.0 || r_diff < -0.5)
            atten = 5.0;
         else if (r_diff > 0.2 || r_diff < -0.1)
            atten = 14.0;
         else
            atten = 15.0;
      end
   end
   
   always begin
      if (1) begin
         #90;
         r_amp = r_diff;
         if (r_out + r_amp * r_vdd / (atten * 0.5) > r_vdd) begin
            r_out = r_vdd;
         end
         else if (r_out + r_amp * r_vdd / (atten * 0.5) < 1e-6) begin
            r_out = 1e-6;
         end
         else
            r_out = r_out + r_amp * r_vdd / (atten * 0.5);
      end
   end

   initial begin
      $xana_sink (vdd, r_vdd);
      $xana_sink (ip2n2u, r_ip2n2u);
      $xana_sink (inp, r_inp);
      $xana_sink (inn, r_inn);
      $xana_source (out, r_out);
   end

endmodule

## Example 13: ip_vreg_uvs_srtbias
`timescale 1ns/1ns
module ip_vreg_uvs_srtbias (in2p_strt, ip2n0u5, vdd, vss);
       input in2p_strt;
       output [1:0] ip2n0u5;
       inout vdd;
       inout vss;

   real r_vdd;
   real r_in2p_strt;
   real r_ip2n0u5;

   always @(*) begin
      r_ip2n0u5 = 0;
      if (r_vdd > 0.85) begin
         r_ip2n0u5 = r_in2p_strt * -0.25;
      end
   end

   initial begin
      $xana_sink (vdd, r_vdd);
      $xana_sink (in2p_strt, r_in2p_strt);
      $xana_source (ip2n0u5[1], r_ip2n0u5);
      $xana_source (ip2n0u5[0], r_ip2n0u5);
   end

endmodule


## Example 14: ip_anareg_out
`timescale 1ns/1ns
module ip_anareg_out (atbus, avdd, dvdd, pvdd, dig_off, sel_tstvdd_low, set_avdd_0, set_avdd_1, sgnd, tst_avdd, tst_dvdd, vg, vs, vss);
       output atbus;
       inout avdd;
       inout dvdd;
       inout pvdd;
       input dig_off;
       input sel_tstvdd_low;
       input set_avdd_0;
       input set_avdd_1;
       inout sgnd;
       input tst_avdd;
       input tst_dvdd;
       input vg;
       inout vs;
       inout vss;

   real Ra_load = 2e3;
   real Rd_load = 1.5e3;
   real Rd_iddq = 3e6;
   real Rd_idd = 1.6e3;
   real Cd_load = 1.3e-9;

   real Ra_dmos = 75;

   real r_atbus;

   real r_pvdd;

   real r_avdd;
   real r_dvdd;

   real r_vg;

   real r_d;
   real r_s;
   real r_g;
   real r_gs;
   real r_gst;
   real r_Rd;

   real fg;

   real r_s_t;
   real r_s_tt;
   real r_s_cap;

   real r_dvdd_src;

   real r_dvdd_tau = 1000.0;

   bit Iddq = 0;

   always begin
      #76;
      r_d = r_pvdd;
      r_s = r_avdd;
      r_g = r_vg;
      
      r_gst = r_g - r_s;
      r_gs = (r_gst + r_gs) / 2.0;

      fg = r_gs - 1.9;
      if (fg<0)
         r_Rd = Ra_dmos / (2**(fg*12));
      else
         r_Rd = Ra_dmos / ((fg*12) + 1);

      r_s_tt = r_d * Ra_load / (Ra_load + r_Rd) * 0.9 + r_s_t * 0.1;

      r_s_t = ((r_s_tt - r_s_t) > 1e-4 || (r_s_tt - r_s_t) < -1e-4) ? r_s_tt : r_s_t;

   end

   always @(*) begin
      r_avdd = (r_s_cap <= r_s_t) ? r_s_cap : (r_s_t * 0.1 + r_s_cap * 0.9);
      r_dvdd_src = (dig_off) ? 0.0 : r_avdd;
      Rd_load = (Iddq && dig_off === 1'b1) ? Rd_iddq : (Rd_idd * Rd_iddq) / (Rd_idd + Rd_iddq);
      r_dvdd_tau = Rd_load * Cd_load * 1e9;
      r_atbus = 0;
      if (sel_tstvdd_low) begin
         r_atbus = (r_avdd * tst_avdd + r_dvdd * tst_dvdd) * 9.8374/(19.675+19.675+9.8374) / (1 + tst_avdd || tst_dvdd);
      end
      else begin
         r_atbus = r_avdd * tst_avdd;   // + r_dvdd * tst_dvdd)  / (1 + tst_avdd || tst_dvdd);
      end
   end

   ip_decay decay (r_s_cap, r_s_t, 1024.0);

   ip_decay decay_diddq (r_dvdd, r_dvdd_src, r_dvdd_tau);

   assign (supply1, supply0) avdd = (r_avdd > 1.1) ? 1'b1 : 1'b0;

   assign (supply1, supply0) dvdd = (r_dvdd > 1.0) ? 1'b1 : 1'b0;

   initial begin
      $xana_sink (pvdd, r_pvdd);
      $xana_sink (vg, r_vg);
      $xana_source (avdd, r_avdd);
      $xana_source (dvdd, r_dvdd);
      $xana_source (atbus, r_atbus);
   end
endmodule

## Example 15: ip_diag_comp_n_lvt_np
module ip_diag_comp_n_lvt_np (c, ip2n_2u, out, vdd, vm, vp_c, vp_cn, vss);
       input c;
       input ip2n_2u;
       output out;
       inout vdd;
       input vm;
       input vp_c;
       input vp_cn;
       inout vss;

   real r_vdd;
   real r_ip2n_2u;
   real r_vm;
   real r_vp_c;
   real r_vp_cn;
   
   logic state;
   logic state_del;
   
   wire hi, lo;

   assign lo = (r_vdd > 0.39) ? 1'b0 : 1'bx;

   assign hi = (r_vdd > 0.79) ? 1'b1 : (r_vdd > 0.41) ? 1'bz : 1'bx;

   bit cmode;


   assign cmode = r_vp_c >= 0.65 && r_vp_c <= r_vdd && r_vp_cn >= 0.65 && r_vp_cn <= r_vdd || r_vm >= 0.65 && r_vm <= r_vdd;
   
   always @(*) begin
      if (r_vdd < 0.8 || r_ip2n_2u < 0.3e-6 || r_ip2n_2u > 3.2e-6 || !cmode)   // low starter bias limit (0.5uA)
         state = 1'bx;
      else begin
         if (c === 1'b1) begin
            state = r_vp_c > r_vm;
         end
         else begin
            state = r_vp_cn > r_vm;
         end
      end
   end

   always @(state) #600 state_del = state;
   
   assign out = (state_del) ? hi : lo;

   initial begin
      $xana_sink (vdd, r_vdd);
      $xana_sink (ip2n_2u, r_ip2n_2u);
      $xana_sink (vm, r_vm);
      $xana_sink (vp_c, r_vp_c);
      $xana_sink (vp_cn, r_vp_cn);
   end
endmodule

## Example 16 debounce delay circuit: ip_debounce2u
`timescale 1ns/1ns
module ip_debounce2u (digin, digout, vdd, vss);
       input digin;
       output digout;
       inout vdd;
       inout vss;

   real r_vdd;

   logic digin_todel;
   bit debounce;
   logic digin_del;

   always @(*) begin
      digin_todel = 1'bx;
      if (r_vdd > 0.85) begin
         digin_todel = digin;
      end
      else begin
         debounce = 1'b0;
         disable delay;
      end
   end

   always @(digin_todel) begin : delay
      if (! debounce) begin
         if (digin_todel) begin
            debounce = 1'b1;
            #1720;
            debounce = 1'b0;
            digin_del = digin_todel;
         end
         else begin
            digin_del = digin_todel;
         end
      end
   end

   assign digout = (r_vdd > 0.85) ? ~digin_del : 1'bx;

   initial begin
      $xana_sink (vdd, r_vdd);
   end

endmodule

## Example 17 Test DAC: ipktestdacswgp
`timescale 1ns/100ps
module ipktestdacswgp (g_chop, g_chop_n, nbl_iso, sub, vinn, vinp, voutn, voutp, vss);
    input g_chop;
    input g_chop_n;
    input nbl_iso;
    input sub;
    input vinn;
    input vinp;
    output voutn;
    output voutp;
    inout vss;

    real r_vinp;
    real r_vinn;
    real r_voutp;
    real r_voutn;

    always @(*) begin
        #2;		// 2ns delay to allow for all input signals to settle
        if (g_chop_n == 1'b1 && g_chop == 1'b0) begin
           r_voutp <= #2 r_vinp;
           r_voutn <= #2 r_vinn;
        end
        else if (g_chop_n == 1'b0 && g_chop == 1'b1) begin
           r_voutp <= #2 r_vinn;
           r_voutn <= #2 r_vinp;
        end
        else begin
           r_voutp <= #2 0;
           r_voutn <= #2 0;
        end
    end

    initial begin
        $xana_sink   (vinp, r_vinp);
        $xana_sink   (vinn, r_vinn);
        $xana_source (voutp, r_voutp);
        $xana_source (voutn, r_voutn);
    end
endmodule    

## Example 18 Test DAC Amp: iptestdacamp_orig
`timescale 1ns/1ps
module iptestdacamp_orig (en, en_n, hvdd, inn, inp, ip2n1u, nbl_iso, out, sub, vss);
    input en;
    input en_n;
    inout hvdd;
    input inn;
    input inp;
    input ip2n1u;
    input nbl_iso;
    output out;
    input sub;
    inout vss;

    real r_hvdd;
    real r_inn;
    real r_inp;
    real r_ip2n1u;
    real r_out;
  
    assign bias = (r_ip2n1u > 0.6e-6 && r_ip2n1u < 1.4e-6) ? 1 : 0;
  
    always @(*) begin
        #0.01; 
        if (en && !en_n && r_hvdd > 1.35 && bias) begin	  
            r_out <= #0.01 (r_inn + r_inp) / 2.0;
        end
        else begin
            r_out <= #0.01 0; 		// 10 ps delay to break feedback loop
        end
    end
   
    initial begin
        $xana_sink (hvdd, r_hvdd);
        $xana_sink (ip2n1u, r_ip2n1u);
        $xana_sink (inn, r_inn);
        $xana_sink (inp, r_inp);
        $xana_source (out, r_out);
    end
endmodule

## Example 19 Test DAC: iptestdacswgp
`timescale 1ns/100ps
module iptestdacswgp (g_chop, g_chop_n, nbl_iso, sub, vinn, vinp, voutn, voutp, vss);
    input g_chop;
    input g_chop_n;
    input nbl_iso;
    input sub;
    input vinn;
    input vinp;
    output voutn;
    output voutp;
    inout vss;

    real r_vinp;
    real r_vinn;
    real r_voutp;
    real r_voutn;

    always @(*) begin
        #2;		// 2ns delay to allow for all input signals to settle
        if (g_chop_n == 1'b1 && g_chop == 1'b0) begin
           r_voutp <= #2 r_vinp;
           r_voutn <= #2 r_vinn;
        end
        else if (g_chop_n == 1'b0 && g_chop == 1'b1) begin
           r_voutp <= #2 r_vinn;
           r_voutn <= #2 r_vinp;
        end
        else begin
           r_voutp <= #2 0;
           r_voutn <= #2 0;
        end
    end

    initial begin
        $xana_sink   (vinp, r_vinp);
        $xana_sink   (vinn, r_vinn);
        $xana_source (voutp, r_voutp);
        $xana_source (voutn, r_voutn);
    end
endmodule    

## Example 20 Test DAC Amp: iptestdacamp
`timescale 1ns/1ps
module iptestdacamp (en, en_n, hvdd, inn, inp, ip2n1u, nbl_iso, out, sub, vss);
    input en;
    input en_n;
    inout hvdd;
    input inn;
    input inp;
    input ip2n1u;
    input nbl_iso;
    output out;
    input sub;
    inout vss;

    real r_hvdd;
    real r_inn;
    real r_inp;
    real r_ip2n1u;
    real r_out;
  
    assign bias = (r_ip2n1u > 0.6e-6 && r_ip2n1u < 1.4e-6) ? 1 : 0;
  
    always @(*) begin
        #0.01; 
        if (en && !en_n && r_hvdd > 1.35 && bias) begin	  
            r_out <= #0.01 (r_inn + r_inp) / 2.0;
        end
        else begin
            r_out <= #0.01 0; 		// 10 ps delay to break feedback loop
        end
    end
   
    initial begin
        $xana_sink (hvdd, r_hvdd);
        $xana_sink (ip2n1u, r_ip2n1u);
        $xana_sink (inn, r_inn);
        $xana_sink (inp, r_inp);
        $xana_source (out, r_out);
    end
endmodule


## Example 21 Testreceiver: ip_testreceiver_op
`timescale 1ns/1ns
module ip_testreceiver_op (en_n, ip2n2u, out, vdd, vin, vip, vss);
       input en_n;
       input ip2n2u;
       output out;
       inout vdd;
       input vin;
       input vip;
       inout vss;

   real r_vdd;
   real r_ip2n2u;
   real r_vip;
   real r_vin;
   real r_out;

   always @(*) begin
      r_out = r_vdd;
      if (r_vdd > 1.1 && r_ip2n2u > 1.4e-6 && r_ip2n2u < 2.6e-6 && !en_n) begin
         r_out = r_vip;
         if (r_out > r_vdd)
            r_out = r_vdd;
         if (r_out == 0)
            r_out = 0;
      end
   end

   initial begin
      $xana_sink (vdd, r_vdd);
      $xana_sink (ip2n2u, r_ip2n2u);
      $xana_sink (vip, r_vip);
      $xana_sink (vin, r_vin);
      $xana_source (out, r_out);
   end
endmodule

## Example 22 Testreceiver comparator:  ip_testreceiver_komp1
module ip_testreceiver_komp1 (en_n, out, vbiasp, vdd, vdivh, vdivl, vref, vss);
       input en_n;
       output out;
       input vbiasp;
       inout vdd;
       input vdivh;
       input vdivl;
       input vref;
       inout vss;

   real r_vdd;
   real r_vbiasp;
   real r_vref;
   real r_vdivl;
   real r_vdivh;
   
   logic state;
   logic state_del;
   
   wire hi, lo;

   assign lo = (r_vdd > 0.39) ? 1'b0 : 1'bx;

   assign hi = (r_vdd > 0.79) ? 1'b1 : (r_vdd > 0.41) ? 1'bz : 1'bx;

   bit cmode;

   assign cmode = r_vdivl >= 0.25 && r_vdivl <= r_vdd-0.1 && r_vdivh >= 0.25 && r_vdivh <= r_vdd-0.1 || r_vref >= 0.25 && r_vref <= r_vdd-0.1;
   
   always @(*) begin
      if (r_vdd < 0.8 || r_vbiasp < 1.1 || r_vbiasp > r_vdd || !cmode)
         state = 1'bx;
      else begin
         if (en_n)
            state = 1'b0;
         else begin
            if (out === 1'b1) begin
               state = r_vdivl < r_vref;
            end
            else begin
               state = r_vdivh < r_vref;
            end
         end
      end
   end

   always @(state) #12 state_del = state;
   
   assign out = (en_n) ? 1'b0 : (state_del) ? hi : lo;

   initial begin
      $xana_sink (vdd, r_vdd);
      $xana_sink (vref, r_vref);
      $xana_sink (vbiasp, r_vbiasp);
      $xana_sink (vdivl, r_vdivl);
      $xana_sink (vdivh, r_vdivh);
   end
endmodule


## Example 23 Testreceiver biasing:  ip_testreceiver_bias
module ip_testreceiver_bias (en, en_n, in2p2u, vbiasp, vdd, vss);
       input en;
       input en_n;
       input in2p2u;
       output vbiasp;
       inout vdd;
       inout vss;

   real r_vdd;
   real r_in2p2u;
   real r_vbiasp;

   always @(*) begin
      r_vbiasp = 0;
      if (r_vdd > 1.1) begin
         if (!en)
            r_vbiasp = r_vdd;
         else if (!en_n) begin
            r_vbiasp = -r_in2p2u * 0.8e6;
         end
      end
   end

   initial begin
      $xana_sink (vdd, r_vdd);
      $xana_sink (in2p2u, r_in2p2u);
      $xana_source (vbiasp, r_vbiasp);
   end
endmodule

## Example 24 Test DAC resistor ladder:  ip_testrec_testdac_resistor
module ip_testrec_testdac_resistor (rbot, rtop, vss, rn, vdd, vref, vrefhi, vreflo);
       input rbot;
       output [8:1] rn;
       input rtop;
       input vdd;
       output vref;
       output vrefhi;
       output vreflo;
       input vss;

   real Ra = 916.43;

   real r_vdd;
   real r_rtop;
   real r_rbot;
   real r_vref;
   real r_vrefhi;
   real r_vreflo;
   real r_rn [8:1];

   real r_drop;

   int i;

   real r_R_bot2;
   real r_R_bot1;
   real r_R_reflo;
   real r_R_dac [7:1];
   real r_R_bg2;
   real r_R_refhi2;
   real r_R_refhi1;
   real r_R_top;

   always @(*) begin
      r_drop = r_rtop - r_rbot;
      r_vreflo = r_drop * r_R_bot1 / r_R_top;
      r_vrefhi = r_drop * r_R_bg2 / r_R_top;
      r_vref = r_drop * r_R_refhi1 / r_R_top;
      r_rn[8] = r_drop * r_R_reflo / r_R_top;
      for (i=7; i>1; i-= 1)
         r_rn[i] = r_drop * r_R_dac[i] / r_R_top;
   end

   initial begin
      r_R_bot2 = Ra * 24.0;
      r_R_bot1 = r_R_bot2 + 1.0616e3;
      r_R_reflo = r_R_bot1 + 1.3657e3;
      r_R_dac[7] = r_R_reflo + Ra/11.0;
      for (i=7; i>1; i-= 1)
         r_R_dac[i-1] = r_R_dac[i] + Ra/11.0;
      r_R_bg2 = r_R_dac[1] + Ra * 4.0;
      r_R_refhi2 = r_R_bg2 + Ra;
      r_R_refhi1 = r_R_refhi2 + 1.151e3;
      r_R_top = r_R_refhi1 + Ra * 21.0;
      $xana_sink (vdd, r_vdd);
      $xana_sink (rtop, r_rtop);
      $xana_sink (rbot, r_rbot);
      $xana_source (vref, r_vref);
      $xana_source (vrefhi, r_vrefhi);
      $xana_source (vreflo, r_vreflo);
   end

    genvar gi;
    generate
       for (gi=$low(rn); gi<=$high(rn); gi+=1)
          initial $xana_source (rn[gi], r_rn);
    endgenerate

endmodule

## Example 25 Testreceiver input resistor divider: ip_testreceiver_resist_in
module ip_testreceiver_resist_in (en_comp_n, en_resistor_div_n, outpad, vdd, vip1_high, vip1_low, vss);
       input en_comp_n;
       input en_resistor_div_n;
       input outpad;
       inout vdd;
       output vip1_high;
       output vip1_low;
       inout vss;

   real r_vdd;
   real r_outpad;
   real r_vip1_high;
   real r_vip1_low;

   real Ra = 222.86;
   real Rb = 219.71;
   real Rc = 217.82;
   real Rd = 221.6;

   real r_R_vh1;
   real r_R_vm1;
   real r_R_vl1r;
   real r_R_outpad;

   always @(*) begin
      r_vip1_high = 0;
      r_vip1_low = 0;
      if (r_vdd > 0.85 && !en_comp_n) begin
         if (!en_resistor_div_n) begin
            r_vip1_low = r_outpad * r_R_vl1r / r_R_outpad;
            r_vip1_high = r_outpad * r_R_vh1 / r_R_outpad;
         end
         else begin
            r_vip1_high = r_outpad;
            r_vip1_low = r_outpad;
         end
      end
   end

   initial begin
      r_R_vh1 = Ra * 10.0;
      r_R_vm1 = r_R_vh1 + Rb * 12.0;
      r_R_vl1r = r_R_vm1 + Rc * 17.0;
      r_R_outpad = r_R_vl1r + Rd * 26.0 / 2.0;
      $xana_sink (vdd, r_vdd);
      $xana_sink (outpad, r_outpad);
      $xana_source (vip1_high, r_vip1_high);
      $xana_source (vip1_low, r_vip1_low);
   end
endmodule


## Example 26 oscillator: lf_osc
`timescale 1ns/100ps
module lf_osc (clk, clk_n, disable_osc , disable_out, startup_n2p);
       output logic clk;
       output logic clk_n;
       input disable_osc;
       input disable_out;
       input startup_n2p;

   logic start;
   logic run;
   logic stage4p;
   logic stage4n;

   real r_vdd;
   real r_startup_n2p;

   always begin : lf_osc
      wait (run);
      stage4p = 1'b1;
      stage4n = 1'b0;
      #62.5;
      stage4p = 1'b0;
      stage4n = 1'b1;
      #62.5;
   end

   always @(negedge run) begin
      disable lf_osc;
      stage4p = 1'bz;
      stage4n = 1'bz;
   end

   always @(*) begin
      run = 1'b0;
      if (r_vdd > 0.8) begin
         if (r_startup_n2p < -0.8e-6)
            start = 1'b1;
         run = start & ~disable_osc;
         if (disable_out) begin
            clk = 1'b1;
            clk_n = 1'b0;
         end
         else begin
            clk = stage4p;
            clk_n = stage4n;
         end
      end
      else begin
         start = 1'b0;
      end
   end

   initial begin
      $xana_sink (vt_vdd.pin, r_vdd);
      $xana_sink (startup_n2p, r_startup_n2p);
   end
endmodule


## Example 27 Clock monitor:  hm_clkmon
`timescale 1ns/1ns
module hm_clkmon (clk_nok, clk8mhz, clkfast, clkslow, en_clkmon, in2p2ui, tstclkmon);
       input clk8mhz;
       output logic clk_nok;
       input clkfast;
       input clkslow;
       input en_clkmon;
       input [2:1] in2p2ui;
       input [1:0] tstclkmon;

   logic clks;

   realtime clks_prev;
   realtime period;

   real r_vdd;
   real r_in2p2ui_1;
   real r_in2p2ui_2;

   task supervisor;
      #150.1;
      period += 150.1;
      supervisor();
   endtask

   always @(posedge clks) begin
      period = $realtime - clks_prev;
      clks_prev = $realtime;
      disable supervisor;
      fork
         supervisor();
      join_none;
   end

   always @(*) begin
      clks = 1'bz;
      clk_nok = 1'bz;
      if (r_vdd > 0.8) begin
         clks = ~(clkfast & tstclkmon[0] | clk8mhz & ~(tstclkmon[0] | tstclkmon[1]) | clkslow & ~(tstclkmon[0] | ~tstclkmon[1]));
         clk_nok = 0;
         if (r_in2p2ui_1 + r_in2p2ui_2 > 2.8e-6 && r_in2p2ui_1 + r_in2p2ui_2 < 5.2e-6 && en_clkmon) begin
            clk_nok = period < 80.0 || period > 150.0;   //error if < 6,6MHz or >12,5MHz
         end
      end
   end

   initial begin
      $xana_sink (vt_vdd.pin, r_vdd);
      $xana_sink (in2p2ui[1], r_in2p2ui_1);
      $xana_sink (in2p2ui[2], r_in2p2ui_2);
   end

endmodule


## Example 28 start oscillator: hy_startup_osc_4
`timescale 1ns/1ns
module hy_startup_osc_4 (clk, fosc, fusi_clk_nok, ibias_p2n, n2p_startup, uv);
       output logic clk;
       input fosc;
       input fusi_clk_nok;
       input ibias_p2n;
       output n2p_startup;
       input uv;

   real r_vdd;
   real r_ibias_p2n;
   real r_n2p_startup;

   logic en;
   logic en_start_osc;
   logic out;

   always begin : start_osc
      wait (en_start_osc);
      out = 1'b0;
      #(700);
      out = 1'b1;
      #(700);
   end

   always @(negedge en_start_osc) begin
      out = 1'bz;
      disable start_osc;
   end

   always @(*) begin
      en = 0;
      en_start_osc = 0;
      r_n2p_startup = 0;
      clk = 1'bz;
      if (r_vdd > 0.8) begin
         r_n2p_startup = r_ibias_p2n * -1.0;
         en = uv | fusi_clk_nok;
         if (en) begin
            if (r_ibias_p2n > 1.4e-6) begin
               en_start_osc = 1'b1;
            end
            clk = out;
         end
         else begin
            clk = fosc;
         end
      end
   end

   initial begin
      $xana_sink (vt_vdd.pin, r_vdd);
      $xana_sink (ibias_p2n, r_ibias_p2n);
      $xana_source (n2p_startup, r_n2p_startup);
   end
endmodule

## Example 29 oscillator:  ip_osc
`timescale 1ns/100ps
module ip_osc (clk, clk_n, disable_osc , ip2n_ctat, ip2n_ptat, vdd, vss);
       output logic clk;
       output logic clk_n;
       input disable_osc ;
       input ip2n_ctat;
       input ip2n_ptat;
       inout vdd;
       inout vss;

   logic start;
   logic run;
   logic stage4p;
   logic stage4n;

   real r_vdd;
   real r_ip2n_ctat;
   real r_ip2n_ptat;

   always begin : lf_osc
      wait (run);
      stage4p = 1'b1;
      stage4n = 1'b0;
      #56.0;
      stage4p = 1'b0;
      stage4n = 1'b1;
      #56.0;
   end

   always @(negedge run) begin
      disable lf_osc;
      stage4p = 1'bz;
      stage4n = 1'bz;
   end

   always @(*) begin
      run = 1'b0;
      if (r_vdd > 0.8) begin
         if (r_ip2n_ptat > 0.8e-6 && r_ip2n_ptat > 0.8e-6)
            start = 1'b1;
         run = start & ~disable_osc;
         if (disable_osc) begin
            clk = 1'b1;
            clk_n = 1'b0;
         end
         else begin
            clk = stage4p;
            clk_n = stage4n;
         end
      end
      else begin
         start = 1'b0;
      end
   end

   initial begin
      $xana_sink (vdd, r_vdd);
      $xana_sink (ip2n_ctat, r_ip2n_ctat);
      $xana_sink (ip2n_ptat, r_ip2n_ptat);
   end
endmodule


## Example 30 clock monitor supervision:  ip_clkmon
`timescale 1ns/1ns
module ip_clkmon (clk_nok, clk8mhz, clkfast, clkslow, en_clkmon, in2p2ui, tstclkmon, vdd, vss);
       input clk8mhz;
       output logic clk_nok;
       input clkfast;
       input clkslow;
       input en_clkmon;
       input [2:1] in2p2ui;
       input [1:0] tstclkmon;
       inout vdd;
       inout vss;

   logic clks;

   realtime clks_prev;
   realtime period;

   real r_vdd;
   real r_in2p2ui_1;
   real r_in2p2ui_2;

   task supervisor;
      #150.1;
      period += 150.1;
      supervisor();
   endtask

   always @(posedge clks) begin
      period = $realtime - clks_prev;
      clks_prev = $realtime;
      disable supervisor;
      fork
         supervisor();
      join_none;
   end

   always @(*) begin
      clks = 1'bz;
      clk_nok = 1'bz;
      if (r_vdd > 0.8) begin
         clks = ~(clkfast & tstclkmon[0] | clk8mhz & ~(tstclkmon[0] | tstclkmon[1]) | clkslow & ~(tstclkmon[0] | ~tstclkmon[1]));
         clk_nok = 0;
         if (r_in2p2ui_1 + r_in2p2ui_2 > 2.8e-6 && r_in2p2ui_1 + r_in2p2ui_2 < 5.2e-6 && en_clkmon) begin
            clk_nok = period < 80.0 || period > 150.0;   //error if < 6,6MHz or >12,5MHz
         end
      end
   end

   initial begin
      $xana_sink (vdd, r_vdd);
      $xana_sink (in2p2ui[1], r_in2p2ui_1);
      $xana_sink (in2p2ui[2], r_in2p2ui_2);
   end

endmodule

## Example 31 outpad out driver:  hy_outpad_r
module ip_outpad (data_out, en_n, ip2n2u, pad, vdd, vss);
       input data_out;
       input en_n;
       input ip2n2u;
       output pad;
       inout vdd;
       inout vss;
    initial begin

    end
endmodule


## Example 32 outpad out driver: ip_outpad
module ip_outpad (data_out, en_n, gate, in2p2u, pad, vdd, vss);
       input data_out;
       input en_n;
       input gate;
       input [3:0] in2p2u;
       output pad;
       inout vdd;
       inout vss;
    initial begin

    end
endmodule


## Example 33 outpad driver bias: ip_outpad_bias
module ip_outpad_bias (ip2n2u, in2p2u, vdd, vss);
       input ip2n2u;
       output [3:0] in2p2u;
       inout vdd;
       inout vss;
    initial begin

    end
endmodule


## Example 34 outpad out pad: ip_outpad
module ip_outpad (data_out, en_n, gate, in2p2u, pad, vdd, vss);
       input data_out;
       input en_n;
       input gate;
       input [3:0] in2p2u;
       output pad;
       inout vdd;
       inout vss;
    initial begin

    end
endmodule


## Example 35 outpad driver bias: ip_outpad_bias
module ip_outpad_bias (ip2n2u, in2p2u, vdd, vss);
       input ip2n2u;
       output [3:0] in2p2u;
       inout vdd;
       inout vss;
    initial begin

    end
endmodule


## Example 36 hall sensor: iphallsens_hhs
`timescale 1ns/1ns
module iphallsens_hhs (cnw, cne, cse, csw, poly, guard);
       inout cne;
       inout cnw;
       inout cse;
       inout csw;
       inout guard;
       inout poly;

   parameter int id = 0;

   import "DPI" pure function real cos (input real rTheta);
   import "DPI" pure function real fabs (input real val);

   const real pi = 3.14159265358979;

   real r_meas_cnw,r_meas_cne,r_meas_cse,r_meas_csw;
   real r_diff_nwse, r_diff_nesw;
   real r_feed_cnw_v,r_feed_cne_v,r_feed_cse_v,r_feed_csw_v;
   real r_feed_cnw_i,r_feed_cne_i,r_feed_cse_i,r_feed_csw_i;

   real r_Bz;
   real r_phi_Bz;
   real r_vec_Bz;
   real r_Bcoil_z;
   real r_Voff_zns, r_Voff_zew;
   real Temperature;
   real r_Sens_z;   // 5.56e-2 V/V(bias) 1/T
   real r_Tk_z;    // -3.41e-3 1/K

   real r_feed_v;
   real r_vgain = 1.0;

   real r_R_plate = 1.93e3;
   real r_RNE_slice = r_R_plate/4;
   real r_RSE_slice = r_R_plate/4;
   real r_RNW_slice = r_R_plate/4;
   real r_RSW_slice = r_R_plate/4;
   real r_Rat_plate;

   assign r_Rat_plate = r_RNE_slice + r_RSE_slice + r_RNW_slice + r_RSW_slice;

   always @(*) begin
      Temperature = cds_globals.Temperature[id];
      r_Sens_z = cds_globals.Sens[id];
      r_Tk_z = cds_globals.Tk[id];
      r_Voff_zns = cds_globals.Voff_ns[id];
      r_Voff_zew = cds_globals.Voff_ew[id];
      r_Bz = cds_globals.Bz[id];
      r_phi_Bz = cds_globals.phi_Bz[id];
      r_Bcoil_z = cds_globals.Bcoil_z[id];
      r_feed_v = fabs(r_feed_cnw_v - r_feed_cse_v) + fabs(r_feed_cne_v - r_feed_csw_v);
      r_vgain = 1.0 + (r_feed_v - 1.5) * 0.077;   // centered on 3v, 6% increase at 5v application - plates see much less
      if (r_vgain < 0)
         r_vgain = 0;
      r_vec_Bz = r_Bz*cos(2*pi/360*r_phi_Bz);
      r_diff_nwse = r_vgain * r_Sens_z*(1+r_Tk_z*(Temperature-27))*(r_feed_csw_i-r_feed_cne_i)*r_Rat_plate*r_vec_Bz+r_Bcoil_z+r_Voff_zns;
      r_meas_cnw = (r_feed_cne_v + r_feed_csw_v) / 2.0 + r_diff_nwse/2;
      r_meas_cse = (r_feed_cne_v + r_feed_csw_v) / 2.0 - r_diff_nwse/2;
      r_diff_nesw = r_vgain * r_Sens_z*(1+r_Tk_z*(Temperature-27))*(r_feed_cnw_i-r_feed_cse_i)*r_Rat_plate*r_vec_Bz+r_Bcoil_z+r_Voff_zew;
      r_meas_cne = (r_feed_cnw_v + r_feed_cse_v) / 2.0 + r_diff_nesw/2;
      r_meas_csw = (r_feed_cnw_v + r_feed_cse_v) / 2.0 - r_diff_nesw/2;
   end

   initial begin
      $display ("Hall H(Z) Plate :: ip18ga_hall/iphln_l13u_w50u id %0d at %m", id);

      $xana_source (cne, r_meas_cne, r_RNE_slice,             ,             );
      $xana_source (csw, r_meas_csw, r_RSW_slice,             ,             );
      $xana_source (cnw, r_meas_cnw, r_RNW_slice,             ,             );
      $xana_source (cse, r_meas_cse, r_RSE_slice,             ,             );
      $xana_sink   (cnw,           ,          , r_feed_cnw_v, r_feed_cnw_i);
      $xana_sink   (cse,           ,          , r_feed_cse_v, r_feed_cse_i);
      $xana_sink   (cne,           ,          , r_feed_cne_v, r_feed_cne_i);
      $xana_sink   (csw,           ,          , r_feed_csw_v, r_feed_csw_i);
   end
endmodule


## Example 37 hall sensor: iphallsens_vhs
module iphallsens_vhs (north, east, south, west, sub);
       inout north;
       inout east;
       inout south;
       inout west;
       inout sub;

   parameter real c_rot = 0.0;   // rotation angle (anti-clockwise), reverse angle to align axis to frame of reference axis Y
   parameter int id = 0;

   
   import "DPI" pure function real sin (input real rTheta);
   import "DPI" pure function real fabs (input real val);
   
   const real pi = 3.14159265358979;

   real r_meas_n,r_meas_e,r_meas_s,r_meas_w;
   real r_diff_ns, r_diff_ew;
   real r_feed_n_v,r_feed_e_v,r_feed_s_v,r_feed_w_v;
   real r_feed_n_i,r_feed_e_i,r_feed_s_i,r_feed_w_i;
   real r_feed_diff_ns, r_feed_diff_ew;

   real r_Bxy;
   real r_phi_Bxy;
   real r_vec_Bxy;
   real r_Bcoil_xy;
   real r_Voff_ns, r_Voff_ew;
   real Temperature;
   real r_Sens_xy;   // 2.07e-2 V/V(bias) 1/T
   real r_Tk_xy;    // -3.59e-3 1/K

   real r_feed_v;
   real r_vgain = 1.0;

   real r_R_plate = 1.98e3;
   real r_RN_slice = r_R_plate/4;
   real r_RE_slice = r_R_plate/4;
   real r_RS_slice = r_R_plate/4;
   real r_RW_slice = r_R_plate/4;
   real r_Rat_plate;

   assign r_Rat_plate = r_RN_slice + r_RE_slice + r_RS_slice + r_RW_slice;

   always @(*) begin
      Temperature = cds_globals.Temperature[id];
      r_Sens_xy = cds_globals.Sens[id];
      r_Tk_xy = cds_globals.Tk[id];
      r_Voff_ns = cds_globals.Voff_ns[id];
      r_Voff_ew = cds_globals.Voff_ew[id];
      r_Bxy = cds_globals.Bxy[id];
      r_phi_Bxy = cds_globals.phi_Bxy[id];
      r_Bcoil_xy = cds_globals.Bcoil_xy[id];

      r_feed_v = fabs(r_feed_n_v - r_feed_e_v) + fabs(r_feed_s_v - r_feed_w_v);
      r_vgain = 1.0 + (r_feed_v - 1.5) * 0.071;   // centered on 3v, 6% increase at 5v application - plates see much less
      if (r_vgain < 0)
         r_vgain = 0;

      r_vec_Bxy = r_Bxy*sin(2*pi/360*(r_phi_Bxy - c_rot));
      
      r_diff_ns = r_vgain * -r_Sens_xy*(1+r_Tk_xy*(Temperature-27))*(r_feed_w_i-r_feed_e_i)*r_Rat_plate*r_vec_Bxy+r_Bcoil_xy+r_Voff_ns;
      
      r_meas_n = (r_feed_e_v + r_feed_w_v) / 2.0 + r_diff_ns/2;
      r_meas_s = (r_feed_e_v + r_feed_w_v) / 2.0 - r_diff_ns/2;

      r_diff_ew = r_vgain * -r_Sens_xy*(1+r_Tk_xy*(Temperature-27))*(r_feed_n_i-r_feed_s_i)*r_Rat_plate*r_vec_Bxy+r_Bcoil_xy+r_Voff_ew;

      r_meas_e = (r_feed_n_v + r_feed_s_v) / 2.0 + r_diff_ew/2;
      r_meas_w = (r_feed_n_v + r_feed_s_v) / 2.0 - r_diff_ew/2;
   end

   initial begin
      $display ("Hall V(XY) 4*Plates :: ip/iphallsens_vertical id %0d, c_rot %0.1f at %m", id, c_rot);

      $xana_source (east,  r_meas_e, r_RE_slice,           ,           );
      $xana_source (west,  r_meas_w, r_RW_slice,           ,           );
      $xana_source (north, r_meas_n, r_RN_slice,           ,           );
      $xana_source (south, r_meas_s, r_RS_slice,           ,           );
      $xana_sink   (north,         ,          , r_feed_n_v, r_feed_n_i);
      $xana_sink   (south,         ,          , r_feed_s_v, r_feed_s_i);
      $xana_sink   (east,          ,          , r_feed_e_v, r_feed_e_i);
      $xana_sink   (west,          ,          , r_feed_w_v, r_feed_w_i);
   end
endmodule

## Example 38 hall sensor dummy: iphallsens_vhs_dummy
module iphallsens_vhs_dummy (north, east, south, west, sub);
       inout north;
       inout east;
       inout south;
       inout west;
       inout sub;

   parameter real c_rot = 0.0;   // rotation angle (clockwise), reverse angle to align axis to frame of reference axis Y
   parameter int id = 0;
   
   import "DPI" pure function real sin (input real rTheta);
   
   const real pi = 3.14159265358979;

   real r_meas_n,r_meas_e,r_meas_s,r_meas_w;
   real r_diff_ns, r_diff_ew;
   real r_feed_n_v,r_feed_e_v,r_feed_s_v,r_feed_w_v;
   real r_feed_n_i,r_feed_e_i,r_feed_s_i,r_feed_w_i;
   real r_feed_diff_ns, r_feed_diff_ew;


   real r_Bxy;
   real r_phi_Bxy;
   real r_vec_Bxy;
   real r_Voff_ns, r_Voff_ew;
   real Temperature;
   real r_Sens_xy;   // 1.14e-2 V/V(bias) 1/T
   real r_Tk_xy;    // -1/240 1/K
   
   real r_R_plate = 5e3;
   real r_R_slice = r_R_plate/4;

   always @(*) begin
      Temperature = cds_globals.Temperature[id];
      r_Sens_xy = cds_globals.Sens[id];
      r_Tk_xy = cds_globals.Tk[id];
      r_Voff_ns = cds_globals.Voff_ns[id];
      r_Voff_ew = cds_globals.Voff_ew[id];
      r_Bxy = cds_globals.Bxy[id];
      r_phi_Bxy = cds_globals.phi_Bxy[id];
      
      r_vec_Bxy = r_Bxy*sin(2*pi/360*(r_phi_Bxy+c_rot));
      
      r_diff_ns = r_Sens_xy*(1+r_Tk_xy*(Temperature-27))*(r_feed_w_i-r_feed_e_i)*r_R_plate*r_vec_Bxy+r_Voff_ns;
      
      r_meas_n = (r_feed_e_v + r_feed_w_v) / 2.0 + r_diff_ns/2;
      r_meas_s = (r_feed_e_v + r_feed_w_v) / 2.0 - r_diff_ns/2;

      r_diff_ew = r_Sens_xy*(1+r_Tk_xy*(Temperature-27))*(r_feed_n_i-r_feed_s_i)*r_R_plate*r_vec_Bxy+r_Voff_ew;

      r_meas_e = (r_feed_n_v + r_feed_s_v) / 2.0 + r_diff_ew/2;
      r_meas_w = (r_feed_n_v + r_feed_s_v) / 2.0 - r_diff_ew/2;
   end

   initial begin
      $display ("Hall V(XY) 4*Plates :: ip/iphallsens_vertical id %0d, c_rot %0.1f at %m", id, c_rot);

      $xana_source (east,  r_meas_e, r_R_slice,           ,           );
      $xana_source (west,  r_meas_w, r_R_slice,           ,           );
      $xana_source (north, r_meas_n, r_R_slice,           ,           );
      $xana_source (south, r_meas_s, r_R_slice,           ,           );
      $xana_sink   (north,         ,          , r_feed_n_v, r_feed_n_i);
      $xana_sink   (south,         ,          , r_feed_s_v, r_feed_s_i);
      $xana_sink   (east,          ,          , r_feed_e_v, r_feed_e_i);
      $xana_sink   (west,          ,          , r_feed_w_v, r_feed_w_i);
   end
endmodule

## Example 39 pad bias: ipadbias
module ipadbias (en, ip2n2u_i, ip2n2u_o, ip2n7u_o, tst_vcmred, vbg, vcm0v8, vcm0v8buf, vcm1v2, vcm1v2buf, vdd, vss);
       input en;
       input ip2n2u_i;
       output [2:0] ip2n2u_o;
       output ip2n7u_o;
       input tst_vcmred;
       input vbg;
       output vcm0v8;
       output vcm0v8buf;
       output vcm1v2;
       output vcm1v2buf;
       inout vdd;
       inout vss;

   real r_vdd;
   real r_vbg;
   real r_ip2n2u_i;
   real r_ip2n2u_o;
   real r_ip2n7u_o;

   real r_vcm1v2;
   real r_vcm0v8;

   bit ok;

   assign ok = r_vdd > 1.1 && r_ip2n2u_i > 1.2e-6 && r_ip2n2u_i < 2.8e-6;

   always @(*) begin
      r_ip2n2u_o = 0;
      r_ip2n7u_o = 0;
      r_vcm1v2 = 0;
      r_vcm0v8 = 0;
      if (ok && en) begin
         r_ip2n2u_o = r_ip2n2u_i;
         r_ip2n7u_o = r_ip2n2u_i * 7.0/2.0;
         if (tst_vcmred) begin
            r_vcm1v2 = r_vbg * 11.0/12.0;
            r_vcm0v8 = r_vbg * 7.0/12.0;
         end
         else begin
            r_vcm1v2 = r_vbg;
            r_vcm0v8 = r_vbg * 8.0/12.0;
         end
      end
   end

   initial begin
      $xana_sink (vdd, r_vdd);
      $xana_sink (vbg, r_vbg);
      $xana_sink (ip2n2u_i, r_ip2n2u_i);
      $xana_source (ip2n2u_o[0], r_ip2n2u_o);
      $xana_source (ip2n2u_o[1], r_ip2n2u_o);
      $xana_source (ip2n2u_o[2], r_ip2n2u_o);
      $xana_source (ip2n7u_o, r_ip2n7u_o);

      $xana_source (vcm1v2, r_vcm1v2);
      $xana_source (vcm1v2buf, r_vcm1v2);
      $xana_source (vcm0v8, r_vcm0v8);
      $xana_source (vcm0v8buf, r_vcm0v8);
   end
endmodule


## Example 40 pad comparator: ipadcomp
module ipadcomp (latch, vdd, vss, inn, inp, latch_late_n, latch_n, out, res, latch_res, vbiasn);
       input inn;
       input inp;
       input latch;
       input latch_late_n;
       input latch_n;
       input latch_res;
       output logic out;
       input res;
       input vbiasn;
       inout vdd;
       inout vss;

   real r_vdd;
   real r_inn;
   real r_inp;

   real r_vbiasn;

   logic pap;

   logic lat;
   
   bit cmode;
   
   logic hi;
   logic lo;
   
   wire res_t;
   wire res_h;
   assign #1 res_t = res;
   assign res_h = res_t & res;
   
   assign cmode = r_inn > 0.5 && r_inn < r_vdd ||  r_inp > 0.5 && r_inp < r_vdd && r_vbiasn > 0.6;
   
   assign hi = (cmode) ? 1'b1 : 1'bx;
   assign lo = (cmode) ? 1'b0 : 1'bx;
   
   
   wire latch_late;   // changed to ...
   
   always @(*) begin
      if (res) begin
         pap = 1'bz;
      end
      else begin
         pap = (r_inp >= r_inn) ? hi : lo;
      end
   end

   always @(negedge latch_n) begin
      #1;
      if (latch_late_n)
         lat = pap;
   end

   always @(posedge res) begin
      out = lat;
   end

   initial begin
      $xana_sink (vdd, r_vdd);
      $xana_sink (inn, r_inn);
      $xana_sink (inp, r_inp);
      $xana_sink (vbiasn, r_vbiasn);
   end
endmodule


## Example 41 pad comparator bias: ipadcompbias
module ipadcompbias (vdd, vss, vbiasn, vcmo, en, ip2n2u);
       input en;
       input ip2n2u;
       output vbiasn;
       output vcmo;
       inout vdd;
       inout vss;

   real r_vdd;
   real r_ip2n2u;
   real r_vcm1v0;
   real r_vcmo;
   real r_vbiasn;

   always @(*) begin
      r_vbiasn = 0;
      r_vcmo = r_vdd;
      r_vcm1v0 = r_ip2n2u * 500e3;
      if (r_vcm1v0 > r_vdd)
         r_vcm1v0 = r_vdd;
      if (r_vcm1v0 < 0)
         r_vcm1v0 = 0;
      if (r_vdd > 1.1 && r_ip2n2u > 1.2e-6 && r_ip2n2u < 2.8e-6 && en) begin
         r_vcmo = r_vcm1v0 * 1.0;
         r_vbiasn = r_vcm1v0 * 0.9;
      end
   end

   initial begin
      $xana_sink (vdd, r_vdd);
      $xana_sink (ip2n2u, r_ip2n2u);
      $xana_source (vcmo, r_vcmo);
      $xana_source (vbiasn, r_vbiasn);
   end
endmodule

## Example 42 pad comparator: ipadcompthg
module ipadcompthg (charge, charge_n, chopcomp, cn_n1, cn_p1, cp_n1, cp_p1, en, ffen, i_input_n, i_input_p, ip2n_2u, pos, neg, res, vcmo, vcm0v8, vcm1v2, vdd, vinn, vinp, range, latch_n, vss);
       input charge;
       input charge_n;
       input chopcomp;
       output cn_n1;
       output cn_p1;
       output cp_n1;
       output cp_p1;
       input en;
       input ffen;
       input i_input_n;
       input i_input_p;
       input ip2n_2u;
       input pos;
       input neg;
       input res;
       input vcm0v8;
       input vcm1v2;
       input vcmo;
       inout vdd;
       input vinn;
       input vinp;
       input range;
       input latch_n;
       inout vss;

   real r_vdd;
   real r_vcm1v2;
   real r_ip2n_2u;
   real r_vcmo;
   real r_vinp;
   real r_vinn;

   real r_v_i_input_p;
   real r_v_i_input_n;
   real r_i_input_p;
   real r_i_input_n;
   real r_v_input_p;
   real r_v_input_n;

   real r_cp_p1;
   real r_cp_n1;

   real r_cn_p1;
   real r_cn_n1;

   realtime charge_start, charge_period;
   
   real ns_per_fF = 1e-9 / 232.02e-15;

   real r_th;
   
   real r_tl;

   always @(r_vdd) begin
      if (r_vdd > 0.5) begin
         r_th = r_vdd - 1e-6;
         r_tl = 1e-6;
      end
      else begin
         r_th = r_vdd;
         r_tl = 0.0;
      end
   end

   real r_isig_diff;

   real r_iref_diff_1;
   
   real r_vinp_array;
   real r_vinn_array;

   assign r_i_input_p = r_v_i_input_n / (38.349e3 + 38.349e3);
   assign r_i_input_n = r_v_i_input_p / (38.349e3 + 38.349e3);

   assign r_isig_diff = (ffen) ? (r_i_input_p - r_i_input_n)/(4.0) : 0.0;
   
   assign r_iref_diff_1 = (~range) ? (r_ip2n_2u * 0.5) : (r_ip2n_2u * 1.0);

   assign r_vinp_array = (res) ? r_vcm1v2 : (charge) ? r_vinp : r_vinp_array;
   assign r_vinn_array = (res) ? r_vcm1v2 : (charge) ? r_vinn : r_vinn_array;

   always begin
      @(posedge charge);
      charge_start = $realtime;
      r_cn_n1 =  r_vcmo;
      r_cn_p1 =  r_vcmo;
      r_cp_n1 =  r_vcmo;
      r_cp_p1 =  r_vcmo;
   end

   always begin
      @(negedge latch_n);   // this is when the following comparators sample
      charge_period = $realtime - charge_start;
      if (charge_period < 15)
         charge_period = 15;
      if (charge_period > 90)
         charge_period = 90;
      r_cn_n1 = charge_period * ns_per_fF * (r_isig_diff + r_iref_diff_1) + r_vinp_array;
      r_cn_p1 = charge_period * ns_per_fF * (-r_isig_diff + r_iref_diff_1) + r_vinn_array;
      
      r_cp_n1 = charge_period * ns_per_fF * (-r_isig_diff - r_iref_diff_1) + r_vinn_array;
      r_cp_p1 = charge_period * ns_per_fF * (r_isig_diff - r_iref_diff_1) + r_vinp_array;
      
      if (r_cp_p1 > r_th) r_cp_p1 = r_th;
      if (r_cp_p1 < r_tl) r_cp_p1 = r_tl;
      if (r_cn_p1 > r_th) r_cn_p1 = r_th;
      if (r_cn_p1 < r_tl) r_cn_p1 = r_tl;
      if (r_cp_n1 > r_th) r_cp_n1 = r_th;
      if (r_cp_n1 < r_tl) r_cp_n1 = r_tl;
      if (r_cn_n1 > r_th) r_cn_n1 = r_th;
      if (r_cn_n1 < r_tl) r_cn_n1 = r_tl;

   end

   initial begin      
      $xana_sink (vdd, r_vdd);
      $xana_sink (vcm1v2, r_vcm1v2);
      $xana_sink (ip2n_2u, r_ip2n_2u);
      $xana_sink (vcmo, r_vcmo);
      $xana_sink (vinp, r_vinp);
      $xana_sink (vinn, r_vinn);      
      $xana_sink (i_input_p, r_v_i_input_p);
      $xana_sink (i_input_n, r_v_i_input_n);
      $xana_source (cp_p1, r_cp_p1);
      $xana_source (cp_n1, r_cp_n1);
      $xana_source (cn_p1, r_cn_p1);
      $xana_source (cn_n1, r_cn_n1);
   end
endmodule



## QUESTION
{0}
"""
