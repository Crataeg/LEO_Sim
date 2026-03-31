function [cls, meta] = inferTrueClassFromPowers(Ps_mW, Pi_mW, Pj_mW, Pn_mW, cfg)
    % Pseudo label for display / self-check only.
    %
    % New rule:
    % 1) detect whether interference is visible relative to BOTH noise and signal
    % 2) if visible, map jammer morphology by continuous info code
    %
    % This keeps the original 4-class output but avoids labeling extremely weak
    % jammer cases as tone/mod when the spectrogram is effectively "none".

    meta = struct();

    PsEff = max(Ps_mW, 1e-12);
    PiEff = max(Pi_mW, 1e-12);
    PjEff = max(Pj_mW, 1e-12);
    PnEff = max(Pn_mW, 1e-12);

    meta.jsr_dB = 10*log10(PjEff / PsEff);
    meta.isr_dB = 10*log10(PiEff / PsEff);
    meta.inr_dB = 10*log10(max(PiEff, PjEff) / PnEff);

    hasVisibleInterference = ...
        (meta.inr_dB >= cfg.LabelRule.MinInterfOverNoise_dB) && ...
        (meta.jsr_dB >= cfg.LabelRule.MinJamOverSignal_dB || ...
         meta.isr_dB >= cfg.LabelRule.MinCCIOverSignal_dB);
    meta.hasVisibleInterference = hasVisibleInterference;

    if ~hasVisibleInterference
        cls = 'none';
        return;
    end

    if Pj_mW >= Pi_mW && meta.jsr_dB >= cfg.LabelRule.MinJamOverSignal_dB
        w = jammerMixtureWeightsFromInfoCode(cfg.InfoCode);
        [~, ix] = max(w);
        switch ix
            case 1
                cls = 'tone';
            case 2
                cls = 'pbnj';
            otherwise
                cls = 'mod';
        end
    else
        % Co-channel interference is represented by the wideband/modulated class.
        cls = 'mod';
    end
end
