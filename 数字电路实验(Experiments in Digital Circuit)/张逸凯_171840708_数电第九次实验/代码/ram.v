module ram(code, addr);
	input [7:0] code;
	output reg [7:0] addr;
	reg [7:0] ram [255:0];

	initial
	begin
		$readmemh("C:/Users/Kai/Desktop/memoo.txt", ram, 0, 255);
	end

	always
	begin
		addr = ram[code];
	end
endmodule
