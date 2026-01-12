function run_LEO_EMC_Sim()
% 运行生成的Simulink模型，并展示误码率输出

model = 'LEO_EMC_Sim_Simulink';
if ~bdIsLoaded(model)
    load_system(model);
end

% 你可以在这里修改 cfg（外行只改这几行就行）
cfg = evalin('base','cfg');
cfg.emc.type = 1;     % 1同频噪声 2单音 3脉冲 4邻频等效 5同址等效
cfg.emc.JS_dB = -5;
cfg.leo.fD_Hz = 30e3;
cfg.rx.cfoMethod = 2; % 1理想 2前导估计
assignin('base','cfg',cfg);

simOut = sim(model);

errRate = evalin('base','errRate'); %#ok<NASGU>
disp('仿真完成。工作区变量 errRate = [BER, numErr, numBits]');

% 简单展示
er = evalin('base','errRate');
fprintf("BER=%.3e, Errors=%d, Bits=%d\n", er(end,1), er(end,2), er(end,3));
end
