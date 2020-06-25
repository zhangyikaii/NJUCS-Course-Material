
module ALU(choose, t, asel, bsel, out, carry, overflow, ZF, Aeg, Beg, Ceg, Deg, Eeg, Feg);
	input [2:0] choose;
	input [6:0] t;
	input asel, bsel;
	wire [6:0] B, A;
	assign A = (asel == 0) ? t : A;
	assign B = (bsel == 0) ? t : B;
	output reg out, carry, overflow, ZF;
	output reg [6:0] Aeg;
	output reg [6:0] Beg;
	output reg [6:0] Ceg;
	output reg [6:0] Deg;
	output reg [6:0] Eeg;
	output reg [6:0] Feg;
	integer i, a, b;
	reg [6:0] c;
	reg [6:0] result;
	always @(choose or A or B or t)
	case(choose)
		0: begin { carry, result }=A + B;
					out = 0;
					overflow = (A[6] == B[6] && A[6] != result[6]);
					ZF = !(|result);
					case(result % 10)
					0: Eeg=7'b1000000;
					1: Eeg=7'b1111001;
					2: Eeg=7'b0100100;
					3: Eeg=7'b0110000;
					4: Eeg=7'b0011001;
					5: Eeg=7'b0010010;
					6: Eeg=7'b0000010;
					7: Eeg=7'b1111000;
					8: Eeg=7'b1111111;
					9: Eeg=7'b1111011;
					endcase
					case((result / 10) % 10)
					0: Feg=7'b1000000;
					1: Feg=7'b1111001;
					2: Feg=7'b0100100;
					3: Feg=7'b0110000;
					4: Feg=7'b0011001;
					5: Feg=7'b0010010;
					6: Feg=7'b0000010;
					7: Feg=7'b1111000;
					8: Feg=7'b1111111;
					9: Feg=7'b1111011;
					endcase
					case(A % 10)
					0: Aeg=7'b1000000;
					1: Aeg=7'b1111001;
					2: Aeg=7'b0100100;
					3: Aeg=7'b0110000;
					4: Aeg=7'b0011001;
					5: Aeg=7'b0010010;
					6: Aeg=7'b0000010;
					7: Aeg=7'b1111000;
					8: Aeg=7'b1111111;
					9: Aeg=7'b1111011;
					endcase
					case((A / 10) % 10)
					0: Beg=7'b1000000;
					1: Beg=7'b1111001;
					2: Beg=7'b0100100;
					3: Beg=7'b0110000;
					4: Beg=7'b0011001;
					5: Beg=7'b0010010;
					6: Beg=7'b0000010;
					7: Beg=7'b1111000;
					8: Beg=7'b1111111;
					9: Beg=7'b1111011;
					endcase
					
					case(B % 10)
					0: Ceg=7'b1000000;
					1: Ceg=7'b1111001;
					2: Ceg=7'b0100100;
					3: Ceg=7'b0110000;
					4: Ceg=7'b0011001;
					5: Ceg=7'b0010010;
					6: Ceg=7'b0000010;
					7: Ceg=7'b1111000;
					8: Ceg=7'b1111111;
					9: Ceg=7'b1111011;
					endcase
					case((B / 10) % 10)
					0: Deg=7'b1000000;
					1: Deg=7'b1111001;
					2: Deg=7'b0100100;
					3: Deg=7'b0110000;
					4: Deg=7'b0011001;
					5: Deg=7'b0010010;
					6: Deg=7'b0000010;
					7: Deg=7'b1111000;
					8: Deg=7'b1111111;
					9: Deg=7'b1111011;
					endcase
			end
		1: begin for(i = 0; i <= 6; i = i + 1) 
					c[i] = ~B[i];
					{ carry, result } = A + c + 1;
					out = 0;
					if(result[6] == 1)
						result = ((~result) + 1);
						out = 1;
					overflow = (A[6] == c[6] && A[6] != result[6]); 
					ZF = !(|result);
					case(result % 10)
					0: Eeg=7'b1000000;
					1: Eeg=7'b1111001;
					2: Eeg=7'b0100100;
					3: Eeg=7'b0110000;
					4: Eeg=7'b0011001;
					5: Eeg=7'b0010010;
					6: Eeg=7'b0000010;
					7: Eeg=7'b1111000;
					8: Eeg=7'b1111111;
					9: Eeg=7'b1111011;
					endcase
					case((result / 10) % 10)
					0: Feg=7'b1000000;
					1: Feg=7'b1111001;
					2: Feg=7'b0100100;
					3: Feg=7'b0110000;
					4: Feg=7'b0011001;
					5: Feg=7'b0010010;
					6: Feg=7'b0000010;
					7: Feg=7'b1111000;
					8: Feg=7'b1111111;
					9: Feg=7'b1111011;
					endcase
					case(A % 10)
	0: Aeg=7'b1000000;
	1: Aeg=7'b1111001;
	2: Aeg=7'b0100100;
	3: Aeg=7'b0110000;
	4: Aeg=7'b0011001;
	5: Aeg=7'b0010010;
	6: Aeg=7'b0000010;
	7: Aeg=7'b1111000;
	8: Aeg=7'b1111111;
	9: Aeg=7'b1111011;
	endcase
	case((A / 10) % 10)
	0: Beg=7'b1000000;
	1: Beg=7'b1111001;
	2: Beg=7'b0100100;
	3: Beg=7'b0110000;
	4: Beg=7'b0011001;
	5: Beg=7'b0010010;
	6: Beg=7'b0000010;
	7: Beg=7'b1111000;
	8: Beg=7'b1111111;
	9: Beg=7'b1111011;
	endcase
	
	case(B % 10)
	0: Ceg=7'b1000000;
	1: Ceg=7'b1111001;
	2: Ceg=7'b0100100;
	3: Ceg=7'b0110000;
	4: Ceg=7'b0011001;
	5: Ceg=7'b0010010;
	6: Ceg=7'b0000010;
	7: Ceg=7'b1111000;
	8: Ceg=7'b1111111;
	9: Ceg=7'b1111011;
	endcase
	case((B / 10) % 10)
	0: Deg=7'b1000000;
	1: Deg=7'b1111001;
	2: Deg=7'b0100100;
	3: Deg=7'b0110000;
	4: Deg=7'b0011001;
	5: Deg=7'b0010010;
	6: Deg=7'b0000010;
	7: Deg=7'b1111000;
	8: Deg=7'b1111111;
	9: Deg=7'b1111011;
	endcase
	
			end
		2: begin for(i = 0; i <= 6; i = i + 1) result[i] = ~A[i];out = 0; carry = 0; overflow = 0; ZF = !(|result);
		if(result[6] == 1)
				begin
				result = ((~result) + 1);
				out = 1;
				end
		case(result % 10)
					0: Eeg=7'b1000000;
					1: Eeg=7'b1111001;
					2: Eeg=7'b0100100;
					3: Eeg=7'b0110000;
					4: Eeg=7'b0011001;
					5: Eeg=7'b0010010;
					6: Eeg=7'b0000010;
					7: Eeg=7'b1111000;
					8: Eeg=7'b1111111;
					9: Eeg=7'b1111011;
					endcase
					case((result / 10) % 10)
					0: Feg=7'b1000000;
					1: Feg=7'b1111001;
					2: Feg=7'b0100100;
					3: Feg=7'b0110000;
					4: Feg=7'b0011001;
					5: Feg=7'b0010010;
					6: Feg=7'b0000010;
					7: Feg=7'b1111000;
					8: Feg=7'b1111111;
					9: Feg=7'b1111011;
					endcase
	case(A % 10)
	0: Aeg=7'b1000000;
	1: Aeg=7'b1111001;
	2: Aeg=7'b0100100;
	3: Aeg=7'b0110000;
	4: Aeg=7'b0011001;
	5: Aeg=7'b0010010;
	6: Aeg=7'b0000010;
	7: Aeg=7'b1111000;
	8: Aeg=7'b1111111;
	9: Aeg=7'b1111011;
	endcase
	case((A / 10) % 10)
	0: Beg=7'b1000000;
	1: Beg=7'b1111001;
	2: Beg=7'b0100100;
	3: Beg=7'b0110000;
	4: Beg=7'b0011001;
	5: Beg=7'b0010010;
	6: Beg=7'b0000010;
	7: Beg=7'b1111000;
	8: Beg=7'b1111111;
	9: Beg=7'b1111011;
	endcase
	
	case(B % 10)
	0: Ceg=7'b1000000;
	1: Ceg=7'b1111001;
	2: Ceg=7'b0100100;
	3: Ceg=7'b0110000;
	4: Ceg=7'b0011001;
	5: Ceg=7'b0010010;
	6: Ceg=7'b0000010;
	7: Ceg=7'b1111000;
	8: Ceg=7'b1111111;
	9: Ceg=7'b1111011;
	endcase
	case((B / 10) % 10)
	0: Deg=7'b1000000;
	1: Deg=7'b1111001;
	2: Deg=7'b0100100;
	3: Deg=7'b0110000;
	4: Deg=7'b0011001;
	5: Deg=7'b0010010;
	6: Deg=7'b0000010;
	7: Deg=7'b1111000;
	8: Deg=7'b1111111;
	9: Deg=7'b1111011;
	endcase
		end

		3: begin for(i = 0; i <= 6; i = i + 1) result[i] = A[i] & B[i]; out = 0; carry = 0; overflow = 0; ZF = !(|result);
	if(result[6] == 1)
				begin
				result = ((~result) + 1);
				out = 1;
				end
	case(result % 10)
					0: Eeg=7'b1000000;
					1: Eeg=7'b1111001;
					2: Eeg=7'b0100100;
					3: Eeg=7'b0110000;
					4: Eeg=7'b0011001;
					5: Eeg=7'b0010010;
					6: Eeg=7'b0000010;
					7: Eeg=7'b1111000;
					8: Eeg=7'b1111111;
					9: Eeg=7'b1111011;
					endcase
					case((result / 10) % 10)
					0: Feg=7'b1000000;
					1: Feg=7'b1111001;
					2: Feg=7'b0100100;
					3: Feg=7'b0110000;
					4: Feg=7'b0011001;
					5: Feg=7'b0010010;
					6: Feg=7'b0000010;
					7: Feg=7'b1111000;
					8: Feg=7'b1111111;
					9: Feg=7'b1111011;
					endcase
	case(A % 10)
	0: Aeg=7'b1000000;
	1: Aeg=7'b1111001;
	2: Aeg=7'b0100100;
	3: Aeg=7'b0110000;
	4: Aeg=7'b0011001;
	5: Aeg=7'b0010010;
	6: Aeg=7'b0000010;
	7: Aeg=7'b1111000;
	8: Aeg=7'b1111111;
	9: Aeg=7'b1111011;
	endcase
	case((A / 10) % 10)
	0: Beg=7'b1000000;
	1: Beg=7'b1111001;
	2: Beg=7'b0100100;
	3: Beg=7'b0110000;
	4: Beg=7'b0011001;
	5: Beg=7'b0010010;
	6: Beg=7'b0000010;
	7: Beg=7'b1111000;
	8: Beg=7'b1111111;
	9: Beg=7'b1111011;
	endcase
	
	case(B % 10)
	0: Ceg=7'b1000000;
	1: Ceg=7'b1111001;
	2: Ceg=7'b0100100;
	3: Ceg=7'b0110000;
	4: Ceg=7'b0011001;
	5: Ceg=7'b0010010;
	6: Ceg=7'b0000010;
	7: Ceg=7'b1111000;
	8: Ceg=7'b1111111;
	9: Ceg=7'b1111011;
	endcase
	case((B / 10) % 10)
	0: Deg=7'b1000000;
	1: Deg=7'b1111001;
	2: Deg=7'b0100100;
	3: Deg=7'b0110000;
	4: Deg=7'b0011001;
	5: Deg=7'b0010010;
	6: Deg=7'b0000010;
	7: Deg=7'b1111000;
	8: Deg=7'b1111111;
	9: Deg=7'b1111011;
	endcase
	
	end
		4: begin for(i = 0; i <= 6; i = i + 1) result[i] = A[i] | B[i]; out = 0; carry = 0; overflow = 0; ZF = !(|result); 
		if(result[6] == 1)
				begin
				result = ((~result) + 1);
				out = 1;
				end
		case(result % 10)
					0: Eeg=7'b1000000;
					1: Eeg=7'b1111001;
					2: Eeg=7'b0100100;
					3: Eeg=7'b0110000;
					4: Eeg=7'b0011001;
					5: Eeg=7'b0010010;
					6: Eeg=7'b0000010;
					7: Eeg=7'b1111000;
					8: Eeg=7'b1111111;
					9: Eeg=7'b1111011;
					endcase
					case((result / 10) % 10)
					0: Feg=7'b1000000;
					1: Feg=7'b1111001;
					2: Feg=7'b0100100;
					3: Feg=7'b0110000;
					4: Feg=7'b0011001;
					5: Feg=7'b0010010;
					6: Feg=7'b0000010;
					7: Feg=7'b1111000;
					8: Feg=7'b1111111;
					9: Feg=7'b1111011;
					endcase
		case(A % 10)
	0: Aeg=7'b1000000;
	1: Aeg=7'b1111001;
	2: Aeg=7'b0100100;
	3: Aeg=7'b0110000;
	4: Aeg=7'b0011001;
	5: Aeg=7'b0010010;
	6: Aeg=7'b0000010;
	7: Aeg=7'b1111000;
	8: Aeg=7'b1111111;
	9: Aeg=7'b1111011;
	endcase
	case((A / 10) % 10)
	0: Beg=7'b1000000;
	1: Beg=7'b1111001;
	2: Beg=7'b0100100;
	3: Beg=7'b0110000;
	4: Beg=7'b0011001;
	5: Beg=7'b0010010;
	6: Beg=7'b0000010;
	7: Beg=7'b1111000;
	8: Beg=7'b1111111;
	9: Beg=7'b1111011;
	endcase
	
	case(B % 10)
	0: Ceg=7'b1000000;
	1: Ceg=7'b1111001;
	2: Ceg=7'b0100100;
	3: Ceg=7'b0110000;
	4: Ceg=7'b0011001;
	5: Ceg=7'b0010010;
	6: Ceg=7'b0000010;
	7: Ceg=7'b1111000;
	8: Ceg=7'b1111111;
	9: Ceg=7'b1111011;
	endcase
	case((B / 10) % 10)
	0: Deg=7'b1000000;
	1: Deg=7'b1111001;
	2: Deg=7'b0100100;
	3: Deg=7'b0110000;
	4: Deg=7'b0011001;
	5: Deg=7'b0010010;
	6: Deg=7'b0000010;
	7: Deg=7'b1111000;
	8: Deg=7'b1111111;
	9: Deg=7'b1111011;
	endcase
	
		end
		5: begin for(i = 0; i <= 6; i = i + 1) result[i] = A[i] ^ B[i]; out = 0; carry = 0; overflow = 0; ZF = !(|result);
		if(result[6] == 1)
				begin
				result = ((~result) + 1);
				out = 1;
				end
		case(result % 10)
					0: Eeg=7'b1000000;
					1: Eeg=7'b1111001;
					2: Eeg=7'b0100100;
					3: Eeg=7'b0110000;
					4: Eeg=7'b0011001;
					5: Eeg=7'b0010010;
					6: Eeg=7'b0000010;
					7: Eeg=7'b1111000;
					8: Eeg=7'b1111111;
					9: Eeg=7'b1111011;
					endcase
					case((result / 10) % 10)
					0: Feg=7'b1000000;
					1: Feg=7'b1111001;
					2: Feg=7'b0100100;
					3: Feg=7'b0110000;
					4: Feg=7'b0011001;
					5: Feg=7'b0010010;
					6: Feg=7'b0000010;
					7: Feg=7'b1111000;
					8: Feg=7'b1111111;
					9: Feg=7'b1111011;
					endcase
		case(A % 10)
	0: Aeg=7'b1000000;
	1: Aeg=7'b1111001;
	2: Aeg=7'b0100100;
	3: Aeg=7'b0110000;
	4: Aeg=7'b0011001;
	5: Aeg=7'b0010010;
	6: Aeg=7'b0000010;
	7: Aeg=7'b1111000;
	8: Aeg=7'b1111111;
	9: Aeg=7'b1111011;
	endcase
	case((A / 10) % 10)
	0: Beg=7'b1000000;
	1: Beg=7'b1111001;
	2: Beg=7'b0100100;
	3: Beg=7'b0110000;
	4: Beg=7'b0011001;
	5: Beg=7'b0010010;
	6: Beg=7'b0000010;
	7: Beg=7'b1111000;
	8: Beg=7'b1111111;
	9: Beg=7'b1111011;
	endcase
	
	case(B % 10)
	0: Ceg=7'b1000000;
	1: Ceg=7'b1111001;
	2: Ceg=7'b0100100;
	3: Ceg=7'b0110000;
	4: Ceg=7'b0011001;
	5: Ceg=7'b0010010;
	6: Ceg=7'b0000010;
	7: Ceg=7'b1111000;
	8: Ceg=7'b1111111;
	9: Ceg=7'b1111011;
	endcase
	case((B / 10) % 10)
	0: Deg=7'b1000000;
	1: Deg=7'b1111001;
	2: Deg=7'b0100100;
	3: Deg=7'b0110000;
	4: Deg=7'b0011001;
	5: Deg=7'b0010010;
	6: Deg=7'b0000010;
	7: Deg=7'b1111000;
	8: Deg=7'b1111111;
	9: Deg=7'b1111011;
	endcase
	
	end
		6: begin if(A > B) result = 0; else if(A < B) result = 1; else if(A==B) result = 2;
		out = 0; carry = 0; overflow = 0; ZF = 0; 
			case(result % 10)
					0: Eeg=7'b1000000;
					1: Eeg=7'b1111001;
					2: Eeg=7'b0100100;
					3: Eeg=7'b0110000;
					4: Eeg=7'b0011001;
					5: Eeg=7'b0010010;
					6: Eeg=7'b0000010;
					7: Eeg=7'b1111000;
					8: Eeg=7'b1111111;
					9: Eeg=7'b1111011;
					endcase
					case((result / 10) % 10)
					0: Feg=7'b1000000;
					1: Feg=7'b1111001;
					2: Feg=7'b0100100;
					3: Feg=7'b0110000;
					4: Feg=7'b0011001;
					5: Feg=7'b0010010;
					6: Feg=7'b0000010;
					7: Feg=7'b1111000;
					8: Feg=7'b1111111;
					9: Feg=7'b1111011;
					endcase
		case(A % 10)
	0: Aeg=7'b1000000;
	1: Aeg=7'b1111001;
	2: Aeg=7'b0100100;
	3: Aeg=7'b0110000;
	4: Aeg=7'b0011001;
	5: Aeg=7'b0010010;
	6: Aeg=7'b0000010;
	7: Aeg=7'b1111000;
	8: Aeg=7'b1111111;
	9: Aeg=7'b1111011;
	endcase
	case((A / 10) % 10)
	0: Beg=7'b1000000;
	1: Beg=7'b1111001;
	2: Beg=7'b0100100;
	3: Beg=7'b0110000;
	4: Beg=7'b0011001;
	5: Beg=7'b0010010;
	6: Beg=7'b0000010;
	7: Beg=7'b1111000;
	8: Beg=7'b1111111;
	9: Beg=7'b1111011;
	endcase
	
	case(B % 10)
	0: Ceg=7'b1000000;
	1: Ceg=7'b1111001;
	2: Ceg=7'b0100100;
	3: Ceg=7'b0110000;
	4: Ceg=7'b0011001;
	5: Ceg=7'b0010010;
	6: Ceg=7'b0000010;
	7: Ceg=7'b1111000;
	8: Ceg=7'b1111111;
	9: Ceg=7'b1111011;
	endcase
	case((B / 10) % 10)
	0: Deg=7'b1000000;
	1: Deg=7'b1111001;
	2: Deg=7'b0100100;
	3: Deg=7'b0110000;
	4: Deg=7'b0011001;
	5: Deg=7'b0010010;
	6: Deg=7'b0000010;
	7: Deg=7'b1111000;
	8: Deg=7'b1111111;
	9: Deg=7'b1111011;
	endcase
		
	end
		7: begin if(A==B) result = 0; else result = 1; out = 0; carry = 0; overflow = 0; ZF = 0; 
			case(result % 10)
					0: Eeg=7'b1000000;
					1: Eeg=7'b1111001;
					2: Eeg=7'b0100100;
					3: Eeg=7'b0110000;
					4: Eeg=7'b0011001;
					5: Eeg=7'b0010010;
					6: Eeg=7'b0000010;
					7: Eeg=7'b1111000;
					8: Eeg=7'b1111111;
					9: Eeg=7'b1111011;
					endcase
					case((result / 10) % 10)
					0: Feg=7'b1000000;
					1: Feg=7'b1111001;
					2: Feg=7'b0100100;
					3: Feg=7'b0110000;
					4: Feg=7'b0011001;
					5: Feg=7'b0010010;
					6: Feg=7'b0000010;
					7: Feg=7'b1111000;
					8: Feg=7'b1111111;
					9: Feg=7'b1111011;
					endcase
		case(A % 10)
	0: Aeg=7'b1000000;
	1: Aeg=7'b1111001;
	2: Aeg=7'b0100100;
	3: Aeg=7'b0110000;
	4: Aeg=7'b0011001;
	5: Aeg=7'b0010010;
	6: Aeg=7'b0000010;
	7: Aeg=7'b1111000;
	8: Aeg=7'b1111111;
	9: Aeg=7'b1111011;
	endcase
	case((A / 10) % 10)
	0: Beg=7'b1000000;
	1: Beg=7'b1111001;
	2: Beg=7'b0100100;
	3: Beg=7'b0110000;
	4: Beg=7'b0011001;
	5: Beg=7'b0010010;
	6: Beg=7'b0000010;
	7: Beg=7'b1111000;
	8: Beg=7'b1111111;
	9: Beg=7'b1111011;
	endcase
	
	case(B % 10)
	0: Ceg=7'b1000000;
	1: Ceg=7'b1111001;
	2: Ceg=7'b0100100;
	3: Ceg=7'b0110000;
	4: Ceg=7'b0011001;
	5: Ceg=7'b0010010;
	6: Ceg=7'b0000010;
	7: Ceg=7'b1111000;
	8: Ceg=7'b1111111;
	9: Ceg=7'b1111011;
	endcase
	case((B / 10) % 10)
	0: Deg=7'b1000000;
	1: Deg=7'b1111001;
	2: Deg=7'b0100100;
	3: Deg=7'b0110000;
	4: Deg=7'b0011001;
	5: Deg=7'b0010010;
	6: Deg=7'b0000010;
	7: Deg=7'b1111000;
	8: Deg=7'b1111111;
	9: Deg=7'b1111011;
	endcase
	
		end
		default begin out = 0; overflow = 0; carry = 0; ZF = 0; result = 0; end
	endcase
endmodule