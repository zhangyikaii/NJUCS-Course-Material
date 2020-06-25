module exp030(x,en,y);
  input [3:0] x;
  input en;
  output reg [1:0]y;
 
  always @(x or en)
  if (en) begin
  case (x)
   4'b0001 : y = 2'b00;
   4'b0010 : y = 2'b01;
   4'b0100 : y = 2'b10;
   4'b1000 : y = 2'b11;
   default: y = 2'bzz;
   endcase
   end
   else y = 2'bzz;
endmodule
