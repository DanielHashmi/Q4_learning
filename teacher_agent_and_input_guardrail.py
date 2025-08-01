from open_router_config import config
from agents import Agent, Runner, input_guardrail, RunContextWrapper, GuardrailFunctionOutput
from pydantic import BaseModel

class CheckGuardrailOutput(BaseModel):
    is_study_related: bool
    student_input: str
    reasoning: str

@input_guardrail
async def check_prompt(ctx: RunContextWrapper, agent: Agent, input: str):
    check_input_agent = Agent(
        name='check_input_agent',
        instructions='You check the input of the student, If they are asking study related question or asking something that they should not ask.',
        output_type=CheckGuardrailOutput
    )
    
    result = (await Runner.run(check_input_agent, f'Student Input: {input}', run_config=config)).final_output_as(CheckGuardrailOutput)
    
    return GuardrailFunctionOutput(
        output_info=f"Reasoning: {result.reasoning}, Student Input: {result.student_input}",
        tripwire_triggered=not result.is_study_related
    )
    
teacher = Agent(
    name='teacher',
    instructions='You are a helpful teacher',
    input_guardrails=[check_prompt]
)

result = Runner.run_sync(teacher, 'I want to change my class timings 😭😭', run_config=config)
print(result.final_output)
