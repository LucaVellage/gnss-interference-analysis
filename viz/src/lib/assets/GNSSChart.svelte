<script>
    import { Plot, Line, AreaY, RuleY, RuleX, Text } from 'svelteplot';
    import { Tween } from 'svelte/motion';

    let { maxDate, index, data, byZone = [] } = $props();

    // Tween for the right edge of x 
    const maxDateTweened = Tween.of(() => maxDate, { duration: 800 });

    // Tween for the left edge: zooms from 2022-02-14 to 2025-01-01 at step 8
    const FULL_START   = new Date("2022-02-14").getTime();
    const ZOOM_START = new Date("2025-01-06").getTime();
    const xStartTarget = $derived(index >= 12 ? ZOOM_START : FULL_START);
    const xStartTweened = Tween.of(() => xStartTarget, { duration: 900 });

    const events = [
        { date: new Date("2022-02-24"), label: "UKR Invasion", showAt: 4  },
        { date: new Date("2023-04-01"), label: "RUS jamming", showAt: 6  },
        { date: new Date("2023-10-07"), label: "Israel-Gaza War", showAt: 8 },
        { date: new Date("2023-10-31"), label: "Red Sea attacks", showAt: 8 },
        { date: new Date("2025-05-07"), label: "Operation Sindoor", showAt: 10 },
        { date: new Date("2025-06-13"), label: "Twelve-Day War", showAt: 10 },
        { date: new Date("2026-02-28"), label: "Iran war", showAt: 13 },
    ];

    const annotations = [
        { date: new Date("2022-04-28"), value: 5,  label: "500K km² ≈ Spain", showAt: 0, hideAt: 3 },
        { date: new Date("2023-06-22"), value: 10, label: "1M km² ≈ Egypt", showAt: 0, hideAt: 3 },
        { date: new Date("2025-08-05"), value: 20, label: "2M km² ≈ Saudi Arabia", showAt: 0, hideAt: 3 },
    ];
    // Annotations visible only at steps 0–1; regional reveal at step 2 replaces them

    // Legend config
    const zoneConfig = {
        "Other":                          { color: "#c8cdd6", label: "Other"                              },
        "South Asia":                     { color: "#7b9e87", label: "South Asia"                         },
        "Arabian Peninsula & Red Sea":    { color: "#c4a35a", label: "Arabian Peninsula & Red Sea"        },
        "Baltic Sea Region":              { color: "#4a7fb5", label: "Baltic Sea"                         },
        "Black Sea & Ukraine":            { color: "#2c5282", label: "Black Sea & Ukraine"                },
        "Eastern Mediterranean & Levant": { color: "#c0622f", label: "Eastern Medit. & Levant"                   },
        "Middle East (Iraq/Iran)":        { color: "#8b1a1a", label: "Middle East (Iraq/Iran) & Persian Gulf" },
    };

    const zones = Object.keys(zoneConfig);

    let visibleData = $derived(
        data.filter(d => d.date <= maxDateTweened.current)
    );

    // Sort by zones
    let visibleZoneRows = $derived((() => {
        const xStart = new Date(xStartTweened.current);
        const xEnd   = maxDateTweened.current;
        const filtered = byZone.filter(d => d.date >= xStart && d.date <= xEnd);
        const zoneOrder = Object.fromEntries(zones.map((z, i) => [z, i]));
        return filtered.sort((a, b) => (zoneOrder[a.zone] ?? 99) - (zoneOrder[b.zone] ?? 99));
    })());

    let visibleAnnotations = $derived(
    annotations.filter(a => index >= a.showAt && index < a.hideAt)
    );
    const annotationTarget = $derived(index < 2 ? 1 : 0);
    const annotationTween  = Tween.of(() => annotationTarget, { duration: 1200 });

    let xDomain = $derived([
        new Date(xStartTweened.current),
        maxDateTweened.current
    ]);

    let showRegional  = $derived(index >= 2);

    // Tweening regional opcacity
    const regionalTarget = $derived(showRegional ? 0.85 : 0);
    const regionalTween  = Tween.of(() => regionalTarget, { duration: 1200 });
    const regionalFill   = $derived(regionalTween.current);

    function midDate(start, end) {
        return new Date((start.getTime() + end.getTime()) / 2);
    }
</script>

<div
    class="chart-wrapper"
    class:regional={showRegional}
>
<Plot
    height={500}
    marginTop={110}
    x={{ domain: xDomain }}
    y={{
        label: "Affected airspace (km²)",
        tickFormat: d => {
            if (d >= 10) return `${d / 10}M km²`;
            if (d > 0)   return `${d * 100}K km²`;
            return "0";
        }
    }}
    title="Global GPS Interference in Aviation"
>
    <RuleY data={[0]} />

    {#each events.filter(e => index >= e.showAt) as event}
        <RuleX data={[event]} x="date" stroke="#e63946" strokeDasharray="4" strokeWidth={1.5} strokeOpacity={0.7} />/>
        <Text
            data={[event]}
            x="date"
            text={() => event.label}
            frameAnchor="top"
            fontSize={9.5}
            fill="#e63946"
            fontWeight={600}
            rotate={-90}
            dy={-8}
            textAnchor="start"
        />
    {/each}

    {#each visibleAnnotations as ann}
        <RuleY data={[ann]} y="value" stroke="#333" strokeWidth={1} strokeDasharray="4" opacity={annotationTween.current} />
        <Text
            data={[{ x: midDate(xDomain[0], xDomain[1]), y: ann.value }]}
            x="x"
            y="y"
            text={() => ann.label}
            frameAnchor="top"
            fontSize={11}
            fill="#333"
            fontWeight="bold"
            dy={4}
            opacity={annotationTween.current}
        />
    {/each}

    <!-- Global area + line --> fades out as regional fades in -->
    <AreaY
        data={visibleData}
        x={d => d.date}
        y={d => d.affected_km2 / 100_000}
        fill="#e63946"
        fillOpacity={0.15 * (1 - regionalFill / 0.85)}
    />
    <Line
        data={visibleData}
        x={d => d.date}
        y={d => d.affected_km2 / 100_000}
        stroke="#e63946"
        strokeWidth={1.5}
        strokeOpacity={1 - regionalFill / 0.85 * 0.75}
    />

    <!-- Regional stacked areas — always in DOM, fillOpacity handled by tween -->
    <AreaY
        data={visibleZoneRows}
        x={d => d.date}
        y={d => d.affected_km2 / 100_000}
        z="zone"
        fill={d => zoneConfig[d.zone]?.color ?? "#ccc"}
        fillOpacity={regionalFill}
    />
</Plot>
</div>

<!-- Zone legend fades in via CSS transition -->
<div class="legend" class:visible={showRegional}>
        {#each [...zones].reverse() as zone}
            {@const cfg = zoneConfig[zone]}
            <span class="legend-item">
                <span class="swatch" style="background:{cfg.color}"></span>
                {cfg.label}
            </span>
        {/each}
</div>

<style>
    :global(.svelteplot text) {
        paint-order: stroke fill;
        stroke: #fcfaf7;
        stroke-width: 6px;
        stroke-linejoin: round;
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
            "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        fill: #181818;
    }

    .legend {
        opacity: 0;
        transition: opacity 1.2s ease;
        display: grid;
        grid-template-columns: repeat(4, auto);
        justify-content: center;
        gap: 0.55rem 1.35rem;
        padding: 0.75rem 1rem 0;
        font-size: 0.75rem;
        font-weight: 600;
        color: #5f5f5f;
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
            "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    .legend.visible {
        opacity: 1;
    }

    .legend-item {
        display: flex;
        align-items: center;
        gap: 0.45rem;
        white-space: nowrap;
    }

    .swatch {
        display: inline-block;
        width: 24px;
        height: 4px;
        border-radius: 999px;
        flex-shrink: 0;
    }

    @media (max-width: 640px) {
        .legend {
            grid-template-columns: repeat(2, auto);
            gap: 0.5rem 1rem;
            font-size: 0.7rem;
        }
    }
</style>