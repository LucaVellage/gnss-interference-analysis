<script>
    import GNSSScroller from '$lib/assets/GNSSScroller.svelte';
    import GNSSChart from '$lib/assets/GNSSChart.svelte';

    let { data } = $props();

    
const sections = [
        // Step 0: full chart, space refs, no events, no regions
        { maxDate: new Date("2026-04-01"), index: 0, title: "", text: "" },

        // Step 1: overall textbox
        {
            maxDate: new Date("2026-04-01"),
            index: 1,
            title: "Affected Airspace Has More Than Tripled",
            text: "From February 2022 until May 2026, the global airspace affected by GPS interference has grown substantially, by 216 % across the full period. On June 18, 2025 the global inference area reached its peak at over 2.2 million km², equivalent to 0.4 % of Earth's surface or the area of Saudi Arabia."
        },

        // Step 2: silent: annot. disappear, global fades
        { maxDate: new Date("2026-04-01"), index: 2, title: "", text: "" },

        // Step 3: regional textbox
        {
            maxDate: new Date("2026-04-01"),
            index: 3,
            title: "Regional Conflict Dynamics",
            text: "However, the numbers show strong regional differences. Interference is concentrated in and around active conflict zones, with the Baltic, Black Sea, and Middle East corridors driving most of the growth."
        },

        // Step 4: Shrink + first marker
        { maxDate: new Date("2022-04-01"), index: 4, title: "", text: "" },


        // Step 5: RUS/UKR textbox
        {
            maxDate: new Date("2022-04-01"),
            index: 5,
            title: "A New Era of Electronic Warfare",
            text: "Russia's invasion of Ukraine marked the beginning of a new era of electronic warfare. GPS jamming, despite being previously used in military operations, started spilling over into civilian airspace over the Baltic and Black Sea, as Russian forces disrupted navigation systems across the frontline."
        },

        // Step 6: silent: grows to May 2023, RUS marker
        { maxDate: new Date("2023-05-01"), index:6, title: "", text: "" },

        // Step 7: Russian jamming textbox
        {
            maxDate: new Date("2023-05-01"),
            index: 7,
            title: "Russian Jamming Expands to the Baltics",
            text: "Russia substantially expanded its GPS jamming capabilities in April 2023 as reported by the <a href=\"https://www.themoscowtimes.com/2023/05/05/russia-expands-gps-signal-jamming-to-15-regions-a81049\">The Moscow Times</a>, intensifying GPS jamming in the airspace of the Baltic Sea. The daily global average of affected airspace increased from ~500,000 km² in 2022 to ~900,000 km² in 2023."
        },

        // Step 8: silent: grows to Nov 2023, Gaza + Red Sea markers
        { maxDate: new Date("2023-11-15"), index: 8, title: "", text: "" },

        // Step 9: Gaza & Red Sea textbox
        {
            maxDate: new Date("2023-11-15"),
            index: 9,
            title: "October 2023: Gaza & Red Sea",
            text: "The Hamas attack on October 7 and Israel's subsequent military campaign introduced a new GPS interference hotspot in the Eastern Mediterranean and Levant. Likewise, Houthi attacks on shipping in the Red Sea triggered additional jamming across the Arabian Peninsula. (Sources: <a href=\"https://www.npr.org/2024/04/16/1245143872/electronic-warfare-is-interfering-with-gps-in-areas-of-gaza\">npr</a>, <a href=\"https://www.spglobal.com/energy/en/news-research/latest-news/shipping/080825-electronic-interference-in-red-sea-hormuz-as-houthis-renew-threats-to-shipping\">S&P Global</a>)."
        },

        // Step 10: silent: grows to Jul 2025, SA markers appear
        { maxDate: new Date("2025-07-15"), index: 10, title: "", text: "" },

        // Step 11: South Asia textbox
		{
		    maxDate: new Date("2025-07-15"),
		    index: 11,
		    title: "Heightening Conflict in South Asia",
		    text: "South Asia has emerged as a persistent GPS interference zone since 2024, driven by two overlapping conflicts. The ongoing civil war in Myanmar since 2021 generated continuous jamming observable across Southeast Asian flight corridors. On the India-Pakistan border, longstanding tensions escalated in May 2025 when India launched Operation Sindoor, triggering four days of drone and missile exchanges, alongside intensified interference patterns. (Sources: <a href=\"https://insightful.co.in/2025/11/06/jamming-and-spoofing-of-civilian-airspace-are-the-days-of-gps-based-navigation-over/\">Insightful Geopolitics</a>, <a href=\"https://www.gnssjamming.com/post/gps-jamming-report-june-2024\">GPS Jamming Report: June 2024</a>)" 
		},

        // Step 12: silent: zoom to 2025–2026
        { maxDate: new Date("2026-04-01"), index: 12, title: "", text: "" },

        // Step 13: silent: Iran marker appears
        { maxDate: new Date("2026-04-01"), index: 13, title: "", text: "" },

        // Step 14: Globals textbox
		{
		    maxDate: new Date("2026-04-01"),
		    index: 13,
		    title: "2026: A Global Interference Crisis",
		    text: "The outbreak of the Iran war in February 2026 marked a severe escalation, closing multiple flight information regions across the Gulf and pushing the 2026 daily average to a peak of 1.7 million km² of affected airspace. By early 2026, no major conflict region is unaffected, accounting in total for about two-thirds of affected airspace."
		},
    ];

</script>

<div class="container">
    <section class="intro">
        <span class="eyebrow">F-hain Times</span>
        <h1>Collateral Airspace: How Modern Conflict Jams the Skies</h1>
        <p <p class="lede">Active conflict zones are shrinking civilian airspace - but beyond visible no-fly zones over battlefields, an invisible threat compounds the crisis. GPS interferences, a tool of modern defence, can render aircraft navigation systems unreliable far beyond the frontline.</p>
        <p class="byline">Luca Vellage & Daniel Boppert · May 6, 2026</p>
        <p class="paragraph">With the invasion of Ukraine in 2022, Russia aggressively began to deploy GPS interference for defence, primarily to disrupt drones and missiles that rely on GPS for navigation. Aircraft navigation builds on the same system, causing aircraft flying near conflict zones to experience sudden, erroneous shifts in their GPS position, potentially causing dangerous miscalculations in crowded airspace. Yet the problem extends well beyond Russia and Ukraine. Data shows that GPS interference has become a regular occurrence across all active regional conflict zones, narrowing the world's safe airspace.</p>
        <p class="paragraph">GPS interference arises primarily through jamming, where a radio frequency intentionally overpowers global navigation satellite systems (GNSS), feeding receivers false position data and distorting their estimated GPS location. Conflict parties regularly deploy jammers to intercept GNSS frequencies across a wide range, like on the Venezuelan island of Monjes del Sur, as the <a href="https://www.nytimes.com/2025/12/20/world/americas/us-venezuela-caribbean-gps-flight-hazard.html">New York Times</a> reports. The radius of interference varies per jammer and terrain with more sophisticated systems capable of reaching far beyond the immediate conflict zone. 
        Russian manufacturer Aviaconversia, for example, markets a GPS jammer with a reach of 200km. </p>
        <p class="paragraph">However, the location and reach of GPS jammers deployed in conflict zones is not publicly known. To estimate the extent of affected airspace, The F-hain Times analysed flight records (ADS-B) published by <a href="https://gpsjam.org">GPSJam.org</a>, aggregating aircraft reporting medium to high GPS interference per 1800 km² patches of airspace, which is approximately the size of London. The full methodology can be read <a href="#methodology">here</a>. </p>
    </section>

    <GNSSScroller {sections}>
        {#snippet background({ section, index })}
            <GNSSChart
                maxDate={section.maxDate}
                {index}
                data={data.daily}
                byZone={data.byZone}
            />
        {/snippet}
    </GNSSScroller>

    <section class="outro">
        <p>With none of the major regional conflicts showing signs of nearing resolution, worldwide GPS interferences will persist and likely grow as conflict parties expand their GPS jamming capabilities. Aviation authorities and airlines face a new operational baseline, where GPS interferences mid-flight become a new normal, putting authorities and manufacturers to work to make navigation systems resilient to jamming.</p>
        <details id="methodology" class="methodology">
            <summary>Methodology</summary>
            <div class="methodology-body">
                <p>Daily GPS interference data was scraped from <a href="https://gpsjam.org">GPSJam.org</a>, a public monitoring service that aggregates ADS-B flight records from <a href="https://globe.adsbexchange.com">ADS-B Exchange</a> to detect GPS signal interference across defined patches of airspace. As defined by GPSJam.org, airspace patches were classified as experiencing interference when more than 2% of aircraft reported degraded signal quality on a given day. The data is structured across a global hexagonal grid at H3 resolution 4, where each cell covers approximately 1,800 km².</p>
                <p>For the visualisation, the number of affected grid cells were counted and multiplied by the cell area to produce an estimate of total affected airspace in km². The graph shows the weekly average of these estimates. Data covers the period from February 14, 2022 to May 1, 2026. Regional breakdowns were produced by assigning each grid cell to a conflict zone of interest based on its geographic coordinates. All code used for scraping, aggregation and analysis is available via <a href="https://github.com/LucaVellage/gnss-interference-analysis">GitHub</a>.</p>
            </div>
        </details>
    </section>
</div>

<svelte:head>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="">
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Source+Serif+4:ital,opsz,wght@0,8..60,300;0,8..60,400;0,8..60,600;1,8..60,300;1,8..60,400&display=swap" rel="stylesheet">
</svelte:head>

<style>
    :global(:root) {
        --bg: rgb(252, 250, 247);
        --surface: #ffffff;
        --text: #181818;
        --muted: #5f5f5f;
        --border: #e6ddd5;
        --accent: #c8642a;
        --accent-soft: #f4e5db;
    }

    :global(body) {
        background: var(--bg);
        margin: 0;
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
            "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: var(--text);
    }

    :global(*) {
        box-sizing: border-box;
    }

    .container {
        max-width: 900px;
        margin: 0 auto;
        padding: 0 1.5rem;
        color: var(--text);
        --content-width: 780px;
    }

    .intro {
        padding: 5.5rem 0 2.5rem;
        margin-bottom: 0;
    }

    .eyebrow,
    h1,
    .lede,
    .paragraph,
    .outro,
    .methodology {
        width: 100%;
        max-width: var(--content-width);
    }

    .eyebrow {
        display: inline-block;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--accent);
        margin-bottom: 1rem;
    }

    h1 {
        font-size: clamp(2.2rem, 4.8vw, 3.4rem);
        font-weight: 800;
        line-height: 1.08;
        letter-spacing: -0.04em;
        margin: 0 0 1.5rem;
        color: var(--text);
    }

    .lede {
        display: block;
        width: 100%;
        max-width: var(--content-width);
        font-size: 1.15rem;
        line-height: 2.15;
        color: #1f1f1f;
        font-weight: 400;
        font-style: normal;
        text-align: justify;
        text-justify: inter-word;
        hyphens: auto;
        overflow-wrap: break-word;
        margin: 0 0 2.25rem;
        padding: 0;
        border: 0;
    }

    .byline {
        font-size: 0.8rem;
        color: #999;
        font-weight: 400;
        letter-spacing: 0.02em;
        margin: -0.75rem 0 1.5rem;
    }

    .lede::after {
        content: '';
        display: block;
        width: 96px;
        height: 3px;
        background: var(--accent);
        margin-top: 1.25rem;
        border-radius: 999px;
    }

    .paragraph {
        font-size: 1rem;
        line-height: 1.9;
        color: var(--muted);
        font-weight: 400;
        text-align: justify;
        text-justify: inter-word;
        hyphens: auto;
        overflow-wrap: break-word;
        margin: 0 0 1.35rem;
    }

    .outro {
        padding: 3rem 0 5rem;
        border-top: 1px solid var(--border);
        margin-top: 2.5rem;
    }

    .outro p {
        width: 100%;
        max-width: var(--content-width);
        font-size: 1rem;
        line-height: 1.85;
        color: var(--muted);
        font-weight: 400;
        text-align: justify;
        text-justify: inter-word;
        hyphens: auto;
        overflow-wrap: break-word;
        margin: 0 0 0.85rem;
    }

    .methodology {
        margin-top: 3rem;
        border-top: 1px solid var(--border);
        padding-top: 1.5rem;
    }

    .methodology summary {
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: var(--accent);
        cursor: pointer;
        list-style: none;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .methodology summary::after {
        content: '▸';
        font-size: 0.7rem;
        transition: transform 0.2s ease;
        color: var(--accent);
    }

    .methodology[open] summary::after {
        transform: rotate(90deg);
    }

    .methodology-body {
        width: 100%;
        max-width: var(--content-width);
        padding-top: 1.25rem;
        font-size: 0.92rem;
        line-height: 1.85;
        color: var(--muted);
        font-weight: 400;
    }

    .methodology-body p {
        text-align: justify;
        text-justify: inter-word;
        hyphens: auto;
        overflow-wrap: break-word;
        margin: 0 0 1rem;
    }

    a {
        color: var(--accent);
        text-decoration: none;
        border-bottom: 1px solid rgba(200, 100, 42, 0.28);
        transition: border-color 0.2s ease, color 0.2s ease;
    }

    a:hover {
        border-bottom-color: var(--accent);
    }

    @media (max-width: 640px) {
        .container {
            padding: 0 1.1rem;
        }

        .intro {
            padding: 4rem 0 2rem;
        }

        .lede {
            font-size: 1.02rem;
            line-height: 2;
        }

        .paragraph,
        .outro p,
        .methodology-body {
            font-size: 0.98rem;
            line-height: 1.8;
        }
    }
</style>