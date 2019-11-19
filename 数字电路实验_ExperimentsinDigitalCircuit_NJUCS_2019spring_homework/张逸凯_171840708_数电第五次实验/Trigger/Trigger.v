module Trigger(in_data,en,clk,out_lock2,out_lock1,clr_n);
input in_data,en,clk,clr_n;
output wire out_lock2,out_lock1;


myasynchro G(in_data,en,clk,out_lock1,clr_n);
mysynchro F(in_data,en,clk,out_lock2,clr_n);

endmodule 