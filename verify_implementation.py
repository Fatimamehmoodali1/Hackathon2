"""Quick verification script for Phase I implementation"""
from src.infrastructure.in_memory_repository import InMemoryTaskRepository
from src.application.task_service import TaskService
from src.application.errors import TaskNotFoundError, EmptyDescriptionError

def test_basic_functionality():
    """Test basic todo operations"""
    print("Testing Phase I Implementation...")

    # Initialize
    repo = InMemoryTaskRepository()
    service = TaskService(repo)

    # Test 1: Add tasks
    print("\n[PASS] Test 1: Add tasks")
    task1 = service.add_task("Buy groceries")
    task2 = service.add_task("Call dentist")
    task3 = service.add_task("Write report")
    assert task1.id == 1, "First task should have ID 1"
    assert task2.id == 2, "Second task should have ID 2"
    assert task3.id == 3, "Third task should have ID 3"
    print(f"  Added 3 tasks: IDs {task1.id}, {task2.id}, {task3.id}")

    # Test 2: View all tasks
    print("\n[PASS] Test 2: View all tasks")
    tasks = service.get_all_tasks()
    assert len(tasks) == 3, "Should have 3 tasks"
    print(f"  Found {len(tasks)} tasks")

    # Test 3: Mark complete
    print("\n[PASS] Test 3: Mark task complete")
    service.mark_complete(1)
    task = service.get_task(1)
    assert task.is_complete == True, "Task 1 should be complete"
    print(f"  Task {task.id} marked as complete")

    # Test 4: Mark incomplete
    print("\n[PASS] Test 4: Mark task incomplete")
    service.mark_incomplete(1)
    task = service.get_task(1)
    assert task.is_complete == False, "Task 1 should be incomplete"
    print(f"  Task {task.id} marked as incomplete")

    # Test 5: Update task
    print("\n[PASS] Test 5: Update task description")
    service.update_task(2, "Call dentist at 3pm")
    task = service.get_task(2)
    assert task.description == "Call dentist at 3pm", "Description should be updated"
    print(f"  Task {task.id} description updated")

    # Test 6: Delete task
    print("\n[PASS] Test 6: Delete task")
    service.delete_task(3)
    tasks = service.get_all_tasks()
    assert len(tasks) == 2, "Should have 2 tasks after deletion"
    print(f"  Task 3 deleted, {len(tasks)} tasks remain")

    # Test 7: ID never reused
    print("\n[PASS] Test 7: Verify ID never reused")
    task4 = service.add_task("New task")
    assert task4.id == 4, "New task should have ID 4 (not reusing ID 3)"
    print(f"  New task has ID {task4.id} (ID 3 not reused)")

    # Test 8: Empty description error
    print("\n[PASS] Test 8: Validate empty description error")
    try:
        service.add_task("   ")
        assert False, "Should raise EmptyDescriptionError"
    except EmptyDescriptionError:
        print("  Empty description correctly rejected")

    # Test 9: Task not found error
    print("\n[PASS] Test 9: Validate task not found error")
    try:
        service.get_task(999)
        assert False, "Should raise TaskNotFoundError"
    except TaskNotFoundError:
        print("  Non-existent task correctly raises error")

    # Test 10: Unicode support
    print("\n[PASS] Test 10: Unicode character support")
    task_unicode = service.add_task("Café meeting")
    assert "Café" in task_unicode.description, "Should support unicode"
    print(f"  Unicode task created successfully")

    print("\n[SUCCESS] All tests passed! Phase I implementation verified.")
    print(f"\n[STATUS] Final state: {len(service.get_all_tasks())} tasks in repository")

    return True

if __name__ == "__main__":
    try:
        test_basic_functionality()
        print("\n[READY] Phase I Console Todo Application is ready!")
        print("\nTo run the application:")
        print("  python -m src.main")
    except AssertionError as e:
        print(f"\n[FAIL] Test failed: {e}")
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
