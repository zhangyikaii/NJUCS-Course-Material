module Timer(clk, en, stop, clear, endone, seg0, seg1);
	input clk;
	input en;
	input stop;
	input clear;
	output reg endone;
	output reg [6:0] seg0;
	output reg [6:0] seg1;
	reg [3:0] h = 0;
	reg [3:0] l = 0;
	reg [6:0] counter = 0;
	reg clk_1s = 0;
	reg [24:0] count_clk = 0;

	always @ (posedge clk)
	begin
		if(count_clk == 25000000)
		begin
			count_clk = 0;
			clk_1s = ~clk_1s;
		end
		else
			count_clk = count_clk + 1;
	end

	always @ (posedge clk_1s)
	begin
	if (en)
	begin
		endone = 0;
		if (clear)
		begin
			counter = 0;
			l = 0;
			h = 0;
		end
		
		else if (stop)
		begin
			counter = counter;
			l = l;
			h = h;
		end
		
		else
		begin
			if (counter > 98)
			begin
				endone = counter % 2;
				counter = counter + 1;
			end
			else
			begin
			counter = counter + 1;
			end
			
			if (counter < 100)
			begin
				l = counter % 10;
				h = ((counter - counter % 10) / 10);
			end
			else
			begin
				l = l;
				h = h;
			end
		end

		case(h)
		0: seg1 = 7'b1000000;
		1: seg1 = 7'b1111001;
		2: seg1 = 7'b0100100;
		3: seg1 = 7'b0110000;
		4: seg1 = 7'b0011001;
		5: seg1 = 7'b0010010;
		6: seg1 = 7'b0000010;
		7: seg1 = 7'b1111000;
		8: seg1 = 7'b0000000;
		9: seg1 = 7'b0010000;
		endcase
		case(l)
		0: seg0 = 7'b1000000;
		1: seg0 = 7'b1111001;
		2: seg0 = 7'b0100100;
		3: seg0 = 7'b0110000;
		4: seg0 = 7'b0011001;
		5: seg0 = 7'b0010010;
		6: seg0 = 7'b0000010;
		7: seg0 = 7'b1111000;
		8: seg0 = 7'b0000000;
		9: seg0 = 7'b0010000;
		endcase
	end
	
	else if (!en)
	begin
		counter = 0;
		l = 0;
		h = 0;
		seg0 = 7'b1000000;
		seg1 = 7'b1000000;
	end
end
endmodule