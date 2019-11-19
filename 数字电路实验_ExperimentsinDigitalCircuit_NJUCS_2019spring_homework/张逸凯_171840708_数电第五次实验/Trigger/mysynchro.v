module mysynchro(in_data,en,clk,out_lock2,clr_n);

input in_data,en,clk,clr_n;
output reg out_lock2;

initial out_lock2 = 0;
 
always @ (posedge clk or negedge clr_n) begin
	if(!clr_n )begin
		if(en) 
				out_lock2 <= 0;
		else
				out_lock2 <= out_lock2;
	end
	else begin 
		if(en)out_lock2 <= in_data;
		else	out_lock2 <= out_lock2;
	end
end

endmodule 