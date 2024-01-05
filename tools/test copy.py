import g4f
import asyncio

gpt4_providers = [
    g4f.Provider.Bing,
    g4f.Provider.Liaobots,
    g4f.Provider.Phind,
]


async def run_provider(provider: g4f.Provider.BaseProvider):
    try:
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": "Hello"}],
            provider=provider,
        )
        print(f"{provider.__name__}:", response)
    except Exception as e:
        print(f"{provider.__name__}:", e)
        
async def run_all():
    calls = [
        run_provider(provider) for provider in gpt4_providers
    ]
    await asyncio.gather(*calls)

asyncio.run(run_all())