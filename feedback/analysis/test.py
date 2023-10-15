s = """- Increase your tone modality: A higher tone modality can greatly enhance student engagement and overall interest in the lecture. Try to vary your tone more, emphasizing important points and using different tones to convey different emotions.

- Increase your speed of speech: A faster pace can help to keep students attentive and focused. Be mindful not to speak too quickly, though, as it may be difficult for some students to keep up. Aim for a moderate increase in your words per minute.

- Incorporate questions throughout the lecture: Asking questions can encourage active participation from students and prompt critical thinking. Introduce thought-provoking questions at appropriate intervals to stimulate discussion and engagement.

- Use a wider range of emotions: To connect with your students and maintain their interest, explore a wider range of emotions in your delivery. Incorporate more positive emotions like happiness and surprise, while also considering when to use calmer or neutral tones.

- Seek feedback from students: Regular feedback from students can provide valuable insights into their learning experience. Consider implementing anonymous feedback surveys or encourage open communication where students can share their thoughts and suggestions for improvement. This will help you better understand their needs and tailor your lectures accordingly.
"""

#print(s.replace('\n','').split('-'))

s = [x.strip() for x in s.replace('\n','').split('-') if x !='']
for i in s:
    print(i)