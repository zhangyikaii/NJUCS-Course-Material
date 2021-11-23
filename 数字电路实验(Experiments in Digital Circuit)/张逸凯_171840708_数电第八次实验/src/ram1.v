module ram1(clk, we, inaddr, outaddr, din, dout);
input clk;
input we;
input [3:0] inaddr;
input [3:0] outaddr;
input [7:0] din;
output reg [7:0] dout;

reg [7:0] ram [15:0];

initial
begin
	$readmemh("C:/Users/Kai/Desktop/memoo.txt", ram, 0, 15);
end

always @(posedge clk)
begin
	if (we)
		ram[inaddr] <= din;
	else
		dout <= ram[outaddr];
	end

endmodule