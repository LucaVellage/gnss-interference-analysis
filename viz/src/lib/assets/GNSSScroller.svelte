<script>
    import SvelteScroller from '@gka/svelte-scroller';
    import { innerHeight } from 'svelte/reactivity/window';

    let { sections, background: scrollBg } = $props();

    let bgHeight = $state(0);
    const top = $derived((innerHeight.current - bgHeight) / 2 / innerHeight.current);
    const bottom = $derived(1 - (innerHeight.current - bgHeight) / 2 / innerHeight.current);

    let count = $state(-1);
    let index = $state(0);
    let offset = $state(0);
    let progress = $state(0);
</script>

<SvelteScroller {top} {bottom} threshold={0.8} query=".step" bind:count bind:index bind:offset bind:progress>
    {#snippet background()}
        <div bind:clientHeight={bgHeight}>
            {@render scrollBg({ index, count, offset, progress, section: sections[index] })}
        </div>
    {/snippet}

    {#snippet foreground()}
        <div class="foreground">
            {#each sections as section}
                <div class="step">
                    {#if section.title || section.text}
                        <div class="card">
                            <h3>{section.title}</h3>
                            <p>{@html section.text}</p>
                        </div>
                    {/if}
                </div>
            {/each}
        </div>
    {/snippet}
</SvelteScroller>

<style>
    .foreground {
        pointer-events: none;
        display: flex;
        flex-direction: column;
        max-width: 420px;
        margin: 0 auto;
        padding: 0 1.25rem;
    }

    .step {
        height: 60vh;
        display: flex;
        align-items: center;
        pointer-events: none;
    }

    .step:first-child {
        margin-top: 45vh;
    }

    .step:last-child {
        margin-bottom: 45vh;
    }

    .card {
        pointer-events: all;
        width: 100%;
        padding: 1.35rem 1.45rem;
        background: rgba(252, 250, 247);
        border: 1px solid #e6ddd5;
        border-top: 3px solid #c8642a;
        border-radius: 0;
        box-shadow: 0 18px 50px rgba(24, 24, 24, 0.08);
        backdrop-filter: blur(14px);
    }

    .card h3 {
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
            "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 0.82rem;
        font-weight: 800;
        line-height: 1.25;
        margin: 0 0 0.7rem;
        color: #c8642a;
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }

    .card p {
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
            "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 0.95rem;
        font-weight: 400;
        line-height: 1.75;
        color: #181818;
        margin: 0;
    }
</style>