import streamlit as st
import psycopg2
from contextlib import closing
from dotenv import load_dotenv
import os

load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

def get_db_connection():
    conn = psycopg2.connect(dbname=DB_NAME, 
                            user=DB_USER, 
                            host=DB_HOST, 
                            password=DB_PASS, 
                            sslmode='require')
    return conn

# Initialize database
def init_db():
    with closing(get_db_connection()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS prompts (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    is_favorite BOOLEAN DEFAULT FALSE
                )
                """
            )
            conn.commit()

# Create a new prompt
def create_prompt(title, description, is_favorite):
    with closing(get_db_connection()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO prompts (title, description, is_favorite) VALUES (%s, %s, %s)",
                (title, description, is_favorite)
            )
            conn.commit()
        
def list_prompts(search_query=None, favorite_filter=None, sort_by='title', sort_order='asc'):
    with closing(get_db_connection()) as conn:
        with conn.cursor() as cur:
            base_query = "SELECT id, title, description, is_favorite FROM prompts"
            conditions = []
            params = []
            
            if search_query:
                conditions.append("title ILIKE %s")
                params.append(f"%{search_query}%")
            
            if favorite_filter is not None:
                conditions.append("is_favorite = %s")
                params.append(favorite_filter)
            
            if conditions:
                base_query += " WHERE " + " AND ".join(conditions)
            
            # Adding sorting to the query
            sort_order_sql = 'ASC' if sort_order == 'asc' else 'DESC'
            if sort_by in ['title', 'is_favorite']:
                base_query += f" ORDER BY {sort_by} {sort_order_sql}"
            
            cur.execute(base_query, tuple(params))
            prompts = cur.fetchall()
            return prompts

# Update a prompt's favorite status
def update_favorite_status(prompt_id, is_favorite):
    with closing(get_db_connection()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE prompts SET is_favorite = %s WHERE id = %s",
                (is_favorite, prompt_id)
            )
            conn.commit()

# Delete a prompt
def delete_prompt(prompt_id):
    with closing(get_db_connection()) as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM prompts WHERE id = %s", (prompt_id,))
            conn.commit()

# Update a prompt
def update_prompt(prompt_id, title, description):
    with closing(get_db_connection()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE prompts SET title = %s, description = %s WHERE id = %s",
                (title, description, prompt_id)
            )
            conn.commit()

# Streamlit UI
def main():
    st.title("Prompt Base")

    # Initialize the database (ensure the table exists)
    init_db()

    # Input form to create a new prompt
    with st.form("prompt_form"):
        title = st.text_input("Prompt Title")
        description = st.text_area("Prompt Description")
        is_favorite = st.checkbox("Favorite")
        submit_button = st.form_submit_button("Create Prompt")

        if submit_button:
            create_prompt(title, description, is_favorite)
            st.success("Prompt Created Successfully!")

    # Search
    st.subheader("Search, Filter and Sort")
    search_query = st.text_input("Search by Title")
    favorite_filter = st.selectbox("Filter by Favorite", options=["All", "Favorite", "Not Favorite"], index=0)
    favorite_filter = True if favorite_filter == "Favorite" else False if favorite_filter == "Not Favorite" else None
    sort_by = st.selectbox("Sort by", options=['title', 'is_favorite'], index=0)
    sort_order = st.selectbox("Sort order", options=['Ascending', 'Descending'], index=0)

    # Display existing prompts and a Clear button
    st.subheader("Saved Prompts")
    # Adjust the call to list_prompts to include the new sorting options
    sort_order_param = 'asc' if sort_order == 'Ascending' else 'desc'
    prompts = list_prompts(search_query=search_query, favorite_filter=favorite_filter, sort_by=sort_by, sort_order=sort_order_param)

    for prompt in prompts:
        prompt_id, prompt_title, prompt_description, prompt_is_favorite = prompt

        # Display each prompt title with an expander to show more details
        with st.expander(prompt_title):
            # edit mode
            edit_mode = st.session_state.get(f'edit_mode_{prompt_id}', False)

            if edit_mode:
                new_title = st.text_input("Title", value=prompt_title, key=f"title_{prompt_id}")
                new_description = st.text_area("Description", value=prompt_description, key=f"desc_{prompt_id}")
                
                if st.button("Save", key=f"save_{prompt_id}"):
                    update_prompt(prompt_id, new_title, new_description)
                    st.session_state[f'edit_mode_{prompt_id}'] = False 
                    st.experimental_rerun()
            else: # not in edit mode
                st.write(f"Description: {prompt_description}")
                # Checkbox
                fav_status = st.checkbox("Favorite", value=prompt_is_favorite, key=f"fav_{prompt_id}")
                if fav_status != prompt_is_favorite:
                    update_favorite_status(prompt_id, fav_status)
                    st.experimental_rerun()

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Edit", key=f"edit_{prompt_id}"):
                        st.session_state[f'edit_mode_{prompt_id}'] = True  # Enter edit mode
                        st.experimental_rerun()

                with col2:
                    if st.button("Delete", key=f"delete_{prompt_id}"):
                        delete_prompt(prompt_id)
                        st.experimental_rerun()



if __name__ == "__main__":
    main()