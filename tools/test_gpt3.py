import g4f
import asyncio

gpt4_providers = [
    g4f.Provider.ChatBase,
    g4f.Provider.FakeGpt,
    g4f.Provider.GptGo,
    g4f.Provider.You,


]

async def run_provider(provider: g4f.Provider.BaseProvider):
    try:
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.gpt_35_turbo,
            messages=[{"role": "user", "content": "Write some code"}],
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