module exp03(x, en, y, flag, seg);
	input [7:0] x;
	input en;
	output reg[2:0] y;
	output reg flag;
	output reg [6:0] seg;
	integer i;
	always @ (x or en)
	begin
		if(x == 0) flag = 0;
		else flag = 1;
		
		if(en) begin
			y = 0;
			for(i = 0; i <= 7; i = i + 1)
			if(x[i]==1) y = i;
		end
		else y = 0;
		case(y)
		0: seg=7'b1000000;
		1: seg=7'b1111001;
		2: seg=7'b0100100;
		3: seg=7'b0110000;
		4: seg=7'b0011001;
		5: seg=7'b0010010;
		6: seg=7'b0000010;
		7: seg=7'b1111000;
		endcase
	end
endmodule
		
	
	