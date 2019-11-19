module exp02(x0,x1,x2,x3,s,y);
	input [1:0] x0,x1,x2,x3,s;
	output reg [1:0] y;
	
	always @ (s or x0 or x1 or x2 or x3)
		case (s)
			0:  y = x0;
			1:  y = x1;
			2:  y = x2;
			3:  y = x3;
			default:y = 2'b00;
		endcase
	
	endmodule
	