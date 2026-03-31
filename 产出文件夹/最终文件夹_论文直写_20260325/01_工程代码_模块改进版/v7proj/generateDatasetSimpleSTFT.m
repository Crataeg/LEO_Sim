function generateDatasetSimpleSTFT(outRoot)
    classes = {'none','tone','pbnj','mod'};
    splits  = {'train','val','test'};
    makeDirs(outRoot, splits, classes);

    % New dataset policy:
    % - keep the same 4 classes
    % - generate samples through the SAME power-aligned IQ synthesizer used
    %   during inference, instead of the old "single jammer template only" path
    % - extend the JSR support to weaker jammer cases
    numTrain = 800;
    numVal   = 160;
    numTest  = 240;

    samplerCfg = defaultPowerAlignedSamplerCfg();
    samplerCfg.Ns = 2048;
    imgSize = samplerCfg.imgSize;

    rng(2026);

    genSplitSimple(outRoot, 'train', classes, numTrain, samplerCfg, imgSize);
    genSplitSimple(outRoot, 'val',   classes, numVal,   samplerCfg, imgSize);
    genSplitSimple(outRoot, 'test',  classes, numTest,  samplerCfg, imgSize);
end
