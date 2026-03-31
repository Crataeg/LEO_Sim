function [selectedSatDefs, meta] = emcLoadExternalConstellationSubset(constCfg, expectedCount, numPlanes, satsPerPlane, Re_m, mu_m3_s2)
%EMCLOADEXTERNALCONSTELLATIONSUBSET Load open constellation data and reshape it
%into a plane-slot subset that the V7 engineering platform can reuse.

    if nargin < 6 || isempty(mu_m3_s2)
        mu_m3_s2 = 3.986004418e14;
    end
    if nargin < 5 || isempty(Re_m)
        Re_m = 6371e3;
    end

    dataFile = getFieldOr(constCfg, 'ExternalDataFile', '');
    if isempty(dataFile)
        error('cfg.Constellation.ExternalDataFile is required when Mode=external.');
    end
    if exist(dataFile, 'file') ~= 2
        error('External constellation data file not found: %s', dataFile);
    end

    extFormat = lower(strtrim(char(string(getFieldOr(constCfg, 'ExternalFormat', 'auto')))));
    if strcmp(extFormat, 'auto')
        [~, ~, ext] = fileparts(dataFile);
        switch lower(ext)
            case '.json'
                extFormat = 'celestrak-json';
            case '.csv'
                extFormat = 'celestrak-csv';
            otherwise
                error('Unsupported external constellation file format: %s', dataFile);
        end
    end

    rawRecords = loadRawRecords(dataFile, extFormat);
    satRecords = normalizeRecords(rawRecords, mu_m3_s2);
    satRecords = satRecords(isfinite([satRecords.SemiMajorAxis_m]) & isfinite([satRecords.Inclination_deg]));
    if numel(satRecords) < expectedCount
        error('External source has only %d usable satellites; %d required.', numel(satRecords), expectedCount);
    end

    targetInc = getFieldOr(constCfg, 'ExternalInclinationTarget_deg', NaN);
    tolInc = getFieldOr(constCfg, 'ExternalInclinationTolerance_deg', NaN);
    if ~isfinite(targetInc)
        targetInc = mean([satRecords.Inclination_deg]);
    end
    if ~isfinite(tolInc) || tolInc <= 0
        tolInc = 2.0;
    end

    inclVec = [satRecords.Inclination_deg];
    raanVec = wrap360Local([satRecords.RAAN_deg]);
    maVec = wrap360Local([satRecords.MeanAnomaly_deg]);
    scoreVec = abs(inclVec - targetInc);

    withinTol = scoreVec <= tolInc;
    candidateRecords = satRecords(withinTol);
    if numel(candidateRecords) < expectedCount
        [~, order] = sortrows([scoreVec(:), raanVec(:), maVec(:)], [1 2 3]);
        candidateRecords = satRecords(order);
    else
        candRaan = wrap360Local([candidateRecords.RAAN_deg]);
        candMa = wrap360Local([candidateRecords.MeanAnomaly_deg]);
        candScore = abs([candidateRecords.Inclination_deg] - targetInc);
        [~, order] = sortrows([candScore(:), candRaan(:), candMa(:)], [1 2 3]);
        candidateRecords = candidateRecords(order);
    end

    selectedRaw = candidateRecords(1:expectedCount);
    selRaan = wrap360Local([selectedRaw.RAAN_deg]);
    selMa = wrap360Local([selectedRaw.MeanAnomaly_deg]);
    [~, order] = sortrows([selRaan(:), selMa(:)], [1 2]);
    selectedRaw = selectedRaw(order);

    selectedSatDefs = repmat(emptySatDef(), 1, expectedCount);
    idx = 0;
    for p = 1:numPlanes
        planeIdx = (p-1) * satsPerPlane + (1:satsPerPlane);
        planeChunk = selectedRaw(planeIdx);
        [~, slotOrder] = sort(wrap360Local([planeChunk.MeanAnomaly_deg]));
        planeChunk = planeChunk(slotOrder);

        for s = 1:satsPerPlane
            idx = idx + 1;
            satDef = planeChunk(s);
            satDef.PlaneIndex = p;
            satDef.SlotIndex = s;
            satDef.Name = sprintf('EXT_P%02d_S%02d_%s', p, s, satDef.NoradId);
            satDef.ApproxAltitude_m = satDef.SemiMajorAxis_m - Re_m;
            selectedSatDefs(idx) = satDef;
        end
    end

    sourceName = char(string(getFieldOr(constCfg, 'ExternalSourceName', '')));
    if isempty(strtrim(sourceName))
        [~, sourceName, ext] = fileparts(dataFile);
        sourceName = [sourceName ext];
    end

    meta = struct();
    meta.Mode = 'external';
    meta.SourceName = sourceName;
    meta.DataFile = dataFile;
    meta.DataFormat = extFormat;
    meta.LoadedSatCount = numel(satRecords);
    meta.SelectedSatCount = numel(selectedSatDefs);
    meta.TargetInclination_deg = targetInc;
    meta.InclinationTolerance_deg = tolInc;
    meta.SemiMajorAxisMean_m = mean([selectedSatDefs.SemiMajorAxis_m]);
    meta.EccentricityMean = mean([selectedSatDefs.Eccentricity]);
    meta.InclinationMean_deg = mean([selectedSatDefs.Inclination_deg]);
    meta.AltitudeMean_km = mean([selectedSatDefs.ApproxAltitude_m]) / 1e3;
    meta.NoradIds = string({selectedSatDefs.NoradId});
end

function rawRecords = loadRawRecords(dataFile, extFormat)
    switch extFormat
        case {'celestrak-json', 'json'}
            rawRecords = jsondecode(fileread(dataFile));
        case {'celestrak-csv', 'csv'}
            rawTable = readtable(dataFile, 'TextType', 'string');
            rawRecords = table2struct(rawTable);
        otherwise
            error('Unsupported external constellation format: %s', extFormat);
    end
end

function satRecords = normalizeRecords(rawRecords, mu_m3_s2)
    n = numel(rawRecords);
    satRecords = repmat(emptySatDef(), 1, n);
    for i = 1:n
        item = rawRecords(i);
        satRecords(i).OriginalName = getStringField(item, 'OBJECT_NAME', sprintf('SAT_%04d', i));
        satRecords(i).ObjectId = getStringField(item, 'OBJECT_ID', '');
        satRecords(i).NoradId = getStringField(item, 'NORAD_CAT_ID', sprintf('%05d', i));
        satRecords(i).Inclination_deg = getNumericField(item, 'INCLINATION', NaN);
        satRecords(i).RAAN_deg = getNumericField(item, 'RA_OF_ASC_NODE', NaN);
        satRecords(i).Eccentricity = getNumericField(item, 'ECCENTRICITY', 0);
        satRecords(i).ArgPerigee_deg = getNumericField(item, 'ARG_OF_PERICENTER', 0);
        satRecords(i).MeanAnomaly_deg = getNumericField(item, 'MEAN_ANOMALY', 0);
        satRecords(i).MeanMotion_rev_per_day = getNumericField(item, 'MEAN_MOTION', NaN);
        satRecords(i).SemiMajorAxis_m = meanMotionToSemiMajorAxis_m(satRecords(i).MeanMotion_rev_per_day, mu_m3_s2);
        satRecords(i).TrueAnomaly_deg = meanToTrueAnomaly_deg(satRecords(i).MeanAnomaly_deg, satRecords(i).Eccentricity);
    end
end

function satDef = emptySatDef()
    satDef = struct( ...
        'Name', '', ...
        'OriginalName', '', ...
        'ObjectId', '', ...
        'NoradId', '', ...
        'SemiMajorAxis_m', NaN, ...
        'ApproxAltitude_m', NaN, ...
        'Eccentricity', NaN, ...
        'Inclination_deg', NaN, ...
        'RAAN_deg', NaN, ...
        'ArgPerigee_deg', NaN, ...
        'MeanAnomaly_deg', NaN, ...
        'TrueAnomaly_deg', NaN, ...
        'MeanMotion_rev_per_day', NaN, ...
        'PlaneIndex', 0, ...
        'SlotIndex', 0);
end

function val = getFieldOr(S, fieldName, defaultVal)
    if isstruct(S) && isfield(S, fieldName) && ~isempty(S.(fieldName))
        val = S.(fieldName);
    else
        val = defaultVal;
    end
end

function txt = getStringField(S, fieldName, defaultTxt)
    if isfield(S, fieldName)
        raw = S.(fieldName);
        if isstring(raw)
            txt = char(raw);
        elseif ischar(raw)
            txt = raw;
        elseif isnumeric(raw)
            txt = sprintf('%g', raw);
        else
            txt = char(string(raw));
        end
        if isempty(strtrim(txt))
            txt = defaultTxt;
        end
    else
        txt = defaultTxt;
    end
end

function val = getNumericField(S, fieldName, defaultVal)
    if isfield(S, fieldName)
        raw = S.(fieldName);
        if isnumeric(raw)
            val = double(raw);
        elseif isstring(raw) || ischar(raw)
            val = str2double(char(raw));
        else
            val = str2double(char(string(raw)));
        end
        if ~isfinite(val)
            val = defaultVal;
        end
    else
        val = defaultVal;
    end
end

function a_m = meanMotionToSemiMajorAxis_m(meanMotion_rev_per_day, mu_m3_s2)
    n_rad_s = meanMotion_rev_per_day * 2 * pi / 86400;
    a_m = (mu_m3_s2 / (n_rad_s^2))^(1/3);
end

function ta_deg = meanToTrueAnomaly_deg(M_deg, ecc)
    M = deg2rad(M_deg);
    if ecc < 1e-10
        ta_deg = wrap360Local(M_deg);
        return;
    end

    E = M;
    for k = 1:12
        E = E - (E - ecc * sin(E) - M) / max(1e-12, 1 - ecc * cos(E));
    end
    ta = 2 * atan2(sqrt(1 + ecc) * sin(E / 2), sqrt(1 - ecc) * cos(E / 2));
    ta_deg = wrap360Local(rad2deg(ta));
end

function ang = wrap360Local(ang)
    ang = mod(ang, 360);
    ang(ang < 0) = ang(ang < 0) + 360;
end
