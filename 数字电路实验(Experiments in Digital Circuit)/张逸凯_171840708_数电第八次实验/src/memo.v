module memo(clk, we, inoutaddr, inoutadd0, din, dout1, dout2);
	input clk;
	input we;
	input [3:0] inoutaddr;
	input [3:0] inoutadd0;
	wire [3:0] addr;
	input [7:0] din;
	output [7:0] dout1;
	output [7:0] dout2;
	assign addr = inoutaddr;
	assign add0 = inoutadd0;
	ram1 S(.clk(clk), .we(we), .inaddr(inoutaddr), .outaddr(addr), .din(din), .dout(dout1));
	ram2port A(.clock(clk), .data(din), .wren(we), .wraddress(inoutadd0), .rdaddress(add0), .q(dout2));
endmodule
