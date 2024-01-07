import g4f
import asyncio
gpt4_providers = [
    g4f.Provider.ChatBase,
    g4f.Provider.FakeGpt,
    g4f.Provider.GptGo,
    g4f.Provider.You,

]
Models_listing = {
        # gpt-3.5
        'gpt-3.5-turbo'          : g4f.models.gpt_35_turbo,
        'gpt-3.5-turbo-0613'     : g4f.models.gpt_35_turbo_0613,
        'gpt-3.5-turbo-16k'      : g4f.models.gpt_35_turbo_16k,
        
        'gpt-3.5-long':  g4f.models.gpt_35_long,
        
        # gpt-4
        'gpt-4'          :  g4f.models.gpt_4,
        'gpt-4-turbo'    :  g4f.models.gpt_4_turbo,

        # Llama 2
        'llama2-7b' :  g4f.models.llama2_7b,
        'llama2-13b':  g4f.models.llama2_13b,
        'llama2-70b':  g4f.models.llama2_70b,
        
        # Mistral
        'mixtral-8x7b':  g4f.models.mixtral_8x7b,
        'mistral-7b':  g4f.models.mistral_7b,
        'openchat_3.5':  g4f.models.openchat_35,
    
    }


async def run_provider(provider):
    try:
        response = await g4f.ChatCompletion.create_async(
            model=provider,
            messages=[{"role": "user", "content": "Hey"}]
        )
        print(f"{provider.name}:", response)
    except Exception as e:
        print(f"{provider.name}:", e)
        # remove the provider from the list of providers to run
async def run_all():
    calls = [
        run_provider(provider) for provider in Models_listing.values()
    ]
    await asyncio.gather(*calls)

asyncio.run(run_all())