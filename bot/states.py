from aiogram.fsm.state import StatesGroup, State

class FeedbackStates(StatesGroup):
    waiting_for_feedback = State()
