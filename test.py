def ch10():
	#Challenge 10: Make the bot speak like someone you know
	st.title("ChatGPT-like clone with Prompt Engineering")

	openai.api_key = st.secrets["openapi_key"]

	prompt_template = """
	"Speak like Yoda from Star Wars for every question that was asked, 
	do not give a direct answer but ask more questions in the style of wise Yoda from Star Wars"
	"""

	if "openai_model" not in st.session_state:
		st.session_state["openai_model"] = "gpt-3.5-turbo"

	if "msg_bot" not in st.session_state:
		st.session_state.msg_bot = []

	for message in st.session_state.msg_bot:
		with st.chat_message(message["role"]):
			st.markdown(message["content"])

	try:

		if prompt := st.chat_input("What is up?"):
			st.session_state.msg_bot.append({"role": "user", "content": prompt})
			with st.chat_message("user"):
				st.markdown(prompt)

			with st.chat_message("assistant"):
				message_placeholder = st.empty()
				full_response = ""
				for response in openai.ChatCompletion.create(
					model=st.session_state["openai_model"],
					messages=[
								{"role": "system", "content": prompt_template},
								{"role": "user", "content": prompt},
							],
					stream=True,
				):
					full_response += response.choices[0].delta.get("content", "")
					message_placeholder.markdown(full_response + "▌")
				message_placeholder.markdown(full_response)
			st.session_state.msg_bot.append({"role": "assistant", "content": full_response})

	except Exception as e:
		st.error(e)