import logging
from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions

PREFIX = 'product_'

@when('I visit the "Home Page"')
def open_home_page(context):
    context.driver.get(context.base_url)

@then('I should see "{message}" in the title')
def verify_title(context, message):
    assert message in context.driver.title

@then('I should not see "{text_string}"')
def verify_absence_of_text(context, text_string):
    assert text_string not in context.driver.find_element(By.TAG_NAME, 'body').text

@when('I set the "{element_name}" to "{text_string}"')
def set_field_value(context, element_name, text_string):
    element = context.driver.find_element(By.ID, PREFIX + element_name.lower().replace(' ', '_'))
    element.clear()
    element.send_keys(text_string)

@when('I select "{text}" in the "{element_name}" dropdown')
def select_dropdown(context, text, element_name):
    element = Select(context.driver.find_element(By.ID, PREFIX + element_name.lower().replace(' ', '_')))
    element.select_by_visible_text(text)

@then('I should see "{text}" in the "{element_name}" dropdown')
def verify_dropdown_selection(context, text, element_name):
    element = Select(context.driver.find_element(By.ID, PREFIX + element_name.lower().replace(' ', '_')))
    assert element.first_selected_option.text == text

@then('the "{element_name}" field should be empty')
def verify_empty_field(context, element_name):
    assert context.driver.find_element(By.ID, PREFIX + element_name.lower().replace(' ', '_')).get_attribute('value') == ''

@when('I copy the "{element_name}" field')
def copy_field(context, element_name):
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.ID, PREFIX + element_name.lower().replace(' ', '_')))
    )
    context.clipboard = element.get_attribute('value')
    logging.info('Clipboard contains: %s', context.clipboard)

@when('I paste the "{element_name}" field')
def paste_field(context, element_name):
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.ID, PREFIX + element_name.lower().replace(' ', '_')))
    )
    element.clear()
    element.send_keys(context.clipboard)

@then('I should see "{text_string}" in the "{element_name}" field')
def verify_field_content(context, text_string, element_name):
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element_value(
            (By.ID, PREFIX + element_name.lower().replace(' ', '_')),
            text_string
        )
    )
    assert found

@when('I change "{element_name}" to "{text_string}"')
def change_field_value(context, element_name, text_string):
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.ID, PREFIX + element_name.lower().replace(' ', '_')))
    )
    element.clear()
    element.send_keys(text_string)

@when('I press the "{button}" button')
def press_button(context, button):
    context.driver.find_element(By.ID, button.lower() + '-btn').click()

@then('I should see "{name}" in the results')
def verify_results_presence(context, name):
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'search_results'),
            name
        )
    )
    assert found

@then('I should not see "{name}" in the results')
def verify_results_absence(context, name):
    assert name not in context.driver.find_element(By.ID, 'search_results').text

@then('I should see the message "{message}"')
def verify_flash_message(context, message):
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'flash_message'),
            message
        )
    )
    assert found
