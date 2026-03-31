function run_V7_starlink_openconst_demo()
%RUN_V7_STARLINK_OPENCONST_DEMO
% Run the baseline synthetic platform and a Starlink-injected platform run,
% then save screenshots, result mats, and comparison plots in a new folder.

    close all;
    clc;

    thisDir = fileparts(mfilename('fullpath'));
    repoRoot = fileparts(thisDir);
    addpath(thisDir);

    stamp = datestr(now, 'yyyymmdd_HHMMSS');
    experimentRoot = fullfile(repoRoot, '成果本身', ['开源星座注入实验_' stamp '_Starlink']);
    dataOutDir = fullfile(experimentRoot, 'data');
    if ~exist(dataOutDir, 'dir')
        mkdir(dataOutDir);
    end

    ensureModelArtifacts(thisDir, repoRoot);

    jsonSrc = fullfile(repoRoot, '成果本身', 'IEICE进化_20260324', 'downloads', 'constellation_data', 'celestrak_starlink_gp_latest_tmp.json');
    tleSrc = fullfile(repoRoot, '成果本身', 'IEICE进化_20260324', 'downloads', 'constellation_data', 'celestrak_starlink_gp_latest_tmp.2le');
    if exist(jsonSrc, 'file') ~= 2
        jsonSrc = fullfile(repoRoot, '成果本身', 'IEICE进化_20260324', 'downloads', 'constellation_data', 'celestrak_starlink_gp.json');
    end
    if exist(tleSrc, 'file') ~= 2
        tleSrc = fullfile(repoRoot, '成果本身', 'IEICE进化_20260324', 'downloads', 'constellation_data', 'celestrak_starlink_gp.2le');
    end

    jsonCopy = fullfile(dataOutDir, ['starlink_open_gp_' stamp '.json']);
    copyfile(jsonSrc, jsonCopy);
    if exist(tleSrc, 'file') == 2
        copyfile(tleSrc, fullfile(dataOutDir, ['starlink_open_gp_' stamp '.2le']));
    end

    baselineDir = fullfile(experimentRoot, '01_baseline_synthetic');
    injectedDir = fullfile(experimentRoot, '02_starlink_injected');

    cfgBase = buildCommonCfg(thisDir, baselineDir);
    cfgBase.General.StartupMode = 'codex-baseline-synthetic';
    resultBase = LEO_StarNet_EMC_V7_0_Engineering(cfgBase);
    exportDashboardSnapshot(resultBase.Dashboard, fullfile(baselineDir, 'baseline_platform_original.png'));
    closePlatformFigure(resultBase);

    cfgExt = buildCommonCfg(thisDir, injectedDir);
    cfgExt.General.StartupMode = 'codex-open-constellation-starlink';
    cfgExt.Constellation.Mode = 'external';
    cfgExt.Constellation.ExternalDataFile = jsonCopy;
    cfgExt.Constellation.ExternalFormat = 'celestrak-json';
    cfgExt.Constellation.ExternalSourceName = 'CelesTrak Starlink GP JSON';
    cfgExt.Constellation.ExternalInclinationTarget_deg = 53;
    cfgExt.Constellation.ExternalInclinationTolerance_deg = 2.0;
    resultExt = LEO_StarNet_EMC_V7_0_Engineering(cfgExt);
    exportDashboardSnapshot(resultExt.Dashboard, fullfile(injectedDir, 'starlink_platform_injected.png'));

    if isfield(resultExt, 'ExternalSatellites')
        selectedTable = struct2table(resultExt.ExternalSatellites);
        writetable(selectedTable, fullfile(injectedDir, 'selected_starlink_subset.csv'), 'Encoding', 'UTF-8');
    end

    makeComparisonFigure(resultBase, resultExt, fullfile(experimentRoot, '03_synthetic_vs_starlink_comparison.png'));
    makeSelectedConstellationFigure(resultExt, fullfile(experimentRoot, '04_starlink_selected_shell.png'));
    writeExperimentSummary(experimentRoot, stamp, jsonCopy, resultBase, resultExt);

    closePlatformFigure(resultExt);
end

function cfg = buildCommonCfg(thisDir, exportDir)
    cfg = emcDefaultConfig();
    cfg.Output.ExportFolder = exportDir;
    cfg.Output.Enable3DViewer = false;
    cfg.Output.AutoSaveResolvedConfig = true;
    cfg.Output.AutoSaveResultMat = true;
    cfg.WorstCase.GAN_modelFile = fullfile(thisDir, 'InfoGAN_Jammer_R2021a.mat');
    cfg.Classifier.ModelFile = fullfile(thisDir, 'lenet_stft_model_r2021a.mat');
    cfg.Classifier.DatasetRoot = fullfile(thisDir, 'dataset_stft_r2021a');
    cfg.Classifier.ExportImages = false;
end

function ensureModelArtifacts(thisDir, repoRoot)
    artifacts = {
        'InfoGAN_Jammer_R2021a.mat', fullfile(repoRoot, '成果本身', '代码工程', 'LEO_Sim', 'LEO_Sim', 'LEO_Sim_V7', 'v7proj', 'InfoGAN_Jammer_R2021a.mat');
        'lenet_stft_model_r2021a.mat', fullfile(repoRoot, '成果本身', '代码工程', 'LEO_Sim', 'LEO_Sim', 'LEO_Sim_V7', 'v7proj', 'lenet_stft_model_r2021a.mat')
        };

    for i = 1:size(artifacts, 1)
        target = fullfile(thisDir, artifacts{i,1});
        if exist(target, 'file') ~= 2
            copyfile(artifacts{i,2}, target);
        end
    end
end

function exportDashboardSnapshot(appFig, outFile)
    if isempty(appFig) || ~isvalid(appFig)
        return;
    end

    drawnow;
    pause(1.0);
    try
        exportapp(appFig, outFile);
    catch
        try
            frame = getframe(appFig);
            imwrite(frame.cdata, outFile);
        catch ME
            warning('Failed to export dashboard snapshot: %s', ME.message);
        end
    end
end

function makeComparisonFigure(resultBase, resultExt, outFile)
    fig = figure('Color', 'w', 'Position', [80 80 1420 860], 'Visible', 'off');
    tl = tiledlayout(fig, 2, 2, 'TileSpacing', 'compact', 'Padding', 'compact');
    title(tl, 'Synthetic V7 vs Starlink-injected V7');

    tb = resultBase.simE2E_Worst.THR;
    te = resultExt.simE2E_Worst.THR;
    xb = linspace(0, numel(tb)-1, numel(tb)) / 6;
    xe = linspace(0, numel(te)-1, numel(te)) / 6;

    nexttile;
    plot(xb, resultBase.simE2E_Base.THR, '--', 'LineWidth', 1.2); hold on;
    plot(xb, resultBase.simE2E_Worst.THR, '-', 'LineWidth', 1.8);
    plot(xe, resultExt.simE2E_Worst.THR, '-', 'LineWidth', 1.8);
    grid on;
    xlabel('Time step / 6');
    ylabel('Mbps');
    title('E2E Throughput');
    legend({'Synthetic Base', 'Synthetic Worst', 'Starlink Worst'}, 'Location', 'best');

    nexttile;
    plot(xb, resultBase.simDL_Worst.SINR, 'LineWidth', 1.5); hold on;
    plot(xe, resultExt.simDL_Worst.SINR, 'LineWidth', 1.5);
    grid on;
    xlabel('Time step / 6');
    ylabel('dB');
    title('DL SINR Worst-case');
    legend({'Synthetic', 'Starlink'}, 'Location', 'best');

    nexttile;
    plot(xb, resultBase.simUL_Worst.THR, 'LineWidth', 1.5); hold on;
    plot(xe, resultExt.simUL_Worst.THR, 'LineWidth', 1.5);
    grid on;
    xlabel('Time step / 6');
    ylabel('Mbps');
    title('UL Throughput Worst-case');
    legend({'Synthetic', 'Starlink'}, 'Location', 'best');

    nexttile;
    bar(categorical({'Synthetic', 'Starlink'}), ...
        [resultBase.simE2E_Worst.meanThr, resultExt.simE2E_Worst.meanThr; ...
         100 * resultBase.simE2E_Worst.outageFrac, 100 * resultExt.simE2E_Worst.outageFrac].');
    grid on;
    ylabel('Value');
    title('Mean Throughput / Outage');
    legend({'MeanThr (Mbps)', 'Outage (%)'}, 'Location', 'best');

    exportgraphics(fig, outFile, 'Resolution', 220);
    close(fig);
end

function makeSelectedConstellationFigure(resultExt, outFile)
    if ~isfield(resultExt, 'ExternalSatellites') || isempty(resultExt.ExternalSatellites)
        return;
    end

    satDefs = resultExt.ExternalSatellites;
    fig = figure('Color', 'w', 'Position', [120 120 1320 520], 'Visible', 'off');
    tl = tiledlayout(fig, 1, 2, 'TileSpacing', 'compact', 'Padding', 'compact');
    title(tl, 'Selected Starlink subset injected into V7');

    nexttile;
    scatter([satDefs.RAAN_deg], [satDefs.ApproxAltitude_m] / 1e3, 24, [satDefs.PlaneIndex], 'filled');
    grid on;
    xlabel('RAAN (deg)');
    ylabel('Approx. Altitude (km)');
    title('RAAN vs Altitude');
    cb = colorbar;
    ylabel(cb, 'Plane index');

    nexttile;
    scatter([satDefs.MeanAnomaly_deg], [satDefs.Inclination_deg], 24, [satDefs.SlotIndex], 'filled');
    grid on;
    xlabel('Mean Anomaly (deg)');
    ylabel('Inclination (deg)');
    title('Mean Anomaly vs Inclination');
    cb = colorbar;
    ylabel(cb, 'Slot index');

    exportgraphics(fig, outFile, 'Resolution', 220);
    close(fig);
end

function writeExperimentSummary(experimentRoot, stamp, jsonFile, resultBase, resultExt)
    fid = fopen(fullfile(experimentRoot, 'README.txt'), 'w');
    if fid < 0
        return;
    end
    cleanupObj = onCleanup(@() fclose(fid)); %#ok<NASGU>

    fprintf(fid, '开源星座注入实验时间: %s\n', stamp);
    fprintf(fid, '数据源: %s\n', jsonFile);
    fprintf(fid, '基线平台: synthetic Walker %dx%d\n', resultBase.cfg.Constellation.NumPlanes, resultBase.cfg.Constellation.SatsPerPlane);
    fprintf(fid, '注入平台: %s\n', resultExt.ConstellationMeta.SourceName);
    fprintf(fid, '注入卫星数: %d\n', numel(resultExt.ExternalSatellites));
    fprintf(fid, '注入平均高度: %.2f km\n', resultExt.ConstellationMeta.AltitudeMean_km);
    fprintf(fid, '基线E2E最坏均值吞吐: %.2f Mbps\n', resultBase.simE2E_Worst.meanThr);
    fprintf(fid, '注入E2E最坏均值吞吐: %.2f Mbps\n', resultExt.simE2E_Worst.meanThr);
    fprintf(fid, '基线E2E最坏中断率: %.2f %%\n', 100 * resultBase.simE2E_Worst.outageFrac);
    fprintf(fid, '注入E2E最坏中断率: %.2f %%\n', 100 * resultExt.simE2E_Worst.outageFrac);
    fprintf(fid, '原始平台截图: 01_baseline_synthetic\\baseline_platform_original.png\n');
    fprintf(fid, '注入平台截图: 02_starlink_injected\\starlink_platform_injected.png\n');
    fprintf(fid, '对比图: 03_synthetic_vs_starlink_comparison.png\n');
    fprintf(fid, '选星分布图: 04_starlink_selected_shell.png\n');
end

function closePlatformFigure(result)
    if isfield(result, 'Dashboard') && ~isempty(result.Dashboard)
        try
            close(result.Dashboard);
        catch
        end
    end
end
