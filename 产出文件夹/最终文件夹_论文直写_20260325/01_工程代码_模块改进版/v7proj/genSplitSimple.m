function genSplitSimple(outRoot, splitName, classes, numPerClass, samplerCfg, imgSize)
    fprintf('  [IntfCls] Split=%s ...\n', splitName);
    kSeed = 0;
    for ci=1:numel(classes)
        cls = classes{ci};
        outDir = fullfile(outRoot, splitName, cls);
        for n=1:numPerClass
            kSeed = kSeed + 1;
            [r, meta] = buildPowerAlignedTrainingSample(cls, samplerCfg, kSeed); %#ok<NASGU>

            img = makeSTFTImageSimple(r, samplerCfg.Stft, imgSize);
            fname = sprintf('%s_%05d_SNR%.1f_JSR%.1f_ISR%.1f.png', ...
                cls, n, meta.snrDb, meta.jsrDb, meta.isrDb);
            imwrite(img, fullfile(outDir, fname));
        end
    end
end

function [r, meta] = buildPowerAlignedTrainingSample(className, samplerCfg, kSeed)
    Ps_mW = 1.0;

    snrList = samplerCfg.Train.SNRdB_list;
    snrDb = snrList(randi(numel(snrList)));
    Pn_mW = Ps_mW / 10^(snrDb/10);

    switch className
        case 'none'
            jsrDb = randRange(samplerCfg.Train.NoneJSR_dB_Range);
            isrDb = randRange(samplerCfg.Train.NoneISR_dB_Range);
            workCfg = samplerCfg;
            workCfg.InfoCode = [0.5 0.5];

        case 'tone'
            jsrDb = randRange(samplerCfg.Train.JamJSR_dB_Range);
            isrDb = randRange(samplerCfg.Train.CCIISR_dB_Range);
            workCfg = samplerCfg;
            workCfg.InfoCode = [0.02 + 0.08*rand, 0.02 + 0.08*rand];

        case 'pbnj'
            jsrDb = randRange(samplerCfg.Train.JamJSR_dB_Range);
            isrDb = randRange(samplerCfg.Train.CCIISR_dB_Range);
            workCfg = samplerCfg;
            workCfg.InfoCode = [0.88 + 0.08*rand, 0.04 + 0.08*rand];

        otherwise  % mod
            jsrDb = randRange(samplerCfg.Train.JamJSR_dB_Range);
            isrDb = randRange(samplerCfg.Train.CCIISR_dB_Range);
            workCfg = samplerCfg;
            workCfg.InfoCode = [0.40 + 0.15*rand, 0.82 + 0.12*rand];
    end

    Pi_mW = Ps_mW * 10^(isrDb/10);
    Pj_mW = Ps_mW * 10^(jsrDb/10);

    [r, meas] = sampleIQFromPowers(Ps_mW, Pi_mW, Pj_mW, Pn_mW, workCfg, kSeed);

    meta = struct();
    meta.snrDb = snrDb;
    meta.jsrDb = jsrDb;
    meta.isrDb = isrDb;
    meta.Ps_meas = meas.Ps_meas;
    meta.Pi_meas = meas.Pi_meas;
    meta.Pj_meas = meas.Pj_meas;
    meta.Pn_meas = meas.Pn_meas;
end

function x = randRange(rg)
    x = rg(1) + (rg(2)-rg(1))*rand;
end
