module shows(
   clkin,
	clken,
	hsync,
	vsync,
	valid,
	vga_sync_n,
	vga_r,
	vga_g,
	vga_b,
	VGA_CLK
				);
				
   input clkin;
	input clken;
	output hsync;
	output vsync;
	output valid;
	output vga_sync_n;
	output [7:0] vga_r;
	output [7:0] vga_g;
	output [7:0] vga_b;
	output VGA_CLK;
wire [11:0] vga_data;
wire [9:0] h_addr;
wire [9:0] v_addr;
wire [18:0]addr;

assign vga_sync_n = 0;
assign addr=v_addr+h_addr*512;
		
				
clkgen #(25000000) vgaclks(clkin,1'b0,1'b1,VGA_CLK);
roms romx(.address(addr), .clock(VGA_CLK), .q(vga_data));

vga_ctrl VGA(
 .pclk(VGA_CLK), //25MHz 时 钟
 .reset(1'b0), //置位
 .vga_data({vga_data}), //上层模块提供的VGA颜色数据
 .h_addr(h_addr), //提供给上层模块的当前扫描像素点坐标 
 .v_addr(v_addr),
 .hsync(hsync), //行同步和列同步信号 
 .vsync(vsync),
 .valid(valid), //消隐信号
 .vga_r(vga_r), //红绿蓝颜色信号 
 .vga_g(vga_g),
 .vga_b(vga_b)
 );	

//always@() 
endmodule 