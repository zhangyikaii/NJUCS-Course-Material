transcript on
if {[file exists rtl_work]} {
	vdel -lib rtl_work -all
}
vlib rtl_work
vmap work rtl_work

vlog -vlog01compat -work work +incdir+E:/My_design/Trigger {E:/My_design/Trigger/mysynchro.v}
vlog -vlog01compat -work work +incdir+E:/My_design/Trigger {E:/My_design/Trigger/myasynchro.v}
vlog -vlog01compat -work work +incdir+E:/My_design/Trigger {E:/My_design/Trigger/Trigger.v}

vlog -vlog01compat -work work +incdir+E:/My_design/Trigger/simulation/modelsim {E:/My_design/Trigger/simulation/modelsim/Trigger.vt}

vsim -t 1ps -L altera_ver -L lpm_ver -L sgate_ver -L altera_mf_ver -L altera_lnsim_ver -L cyclonev_ver -L cyclonev_hssi_ver -L cyclonev_pcie_hip_ver -L rtl_work -L work -voptargs="+acc"  Trigger_vlg_tst

add wave *
view structure
view signals
run -all
