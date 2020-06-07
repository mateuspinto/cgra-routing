module Testbench();

    logic clk, reset;

    initial begin
        $dumpfile("wave.vcd");
        $dumpvars(0, Testbench);
        reset<=1; #3;
        reset<=0; #1;
    end

    always begin
        clk<= 1; #1;
        clk<=0; #1;
    end

    SimpleWriteOnExec simpleWriteOnExec(clk, reset);

endmodule