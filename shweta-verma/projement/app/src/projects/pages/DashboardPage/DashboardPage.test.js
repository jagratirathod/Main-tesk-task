import React from 'react';
import fetchMock from 'fetch-mock';
import { waitForElement, render } from '@testing-library/react';
// import { wait, fireEvent, render  } from '@testing-library/react';
// RouterProvider
import { renderWithContext } from 'core/testUtils';
import { getMockProject } from 'projects/testUtils';
import DashboardPage from './DashboardPage';
import { Provider } from 'react-redux';
import { createMemoryHistory } from 'history';


import { configureStore } from 'core/store';
import { Router } from 'react-router-dom';



describe('DashboardPage', () => {
    beforeEach(() => {
        fetchMock.reset();
    });
    const initialState = {
        isLoading: false
    };
    const store = configureStore(initialState)
    const history = createMemoryHistory();


    console.log(history, 'hisrtory')
    it('fetches and renders a list of projects', async () => {
        // Mock the API request to return a specific list of projects
        fetchMock.getOnce('/api/projects', [
            getMockProject({
                total_estimated_hours: 10,
                total_actual_hours: 5,
            }),
        ]);
       function mockComp(){ return render(<Provider store={store}>
        <Router history={history.location}><DashboardPage/></Router></Provider>)};

        const {getByTestId, getByText} = mockComp()
        await waitForElement(() => getByText('table'));

        expect(getByTestId('project-company-name-0').textContent).toBe(
            'Test Company',
        );
        expect(getByTestId('project-estimated-hours-0').textContent).toBe('10');
        expect(getByTestId('project-actual-hours-0').textContent).toBe('5');
    });

    it('strikes through ended projects', async () => {
        fetchMock.getOnce('/api/projects', [
            getMockProject({ has_ended: true }),
        ]);

        const { getByText } = renderWithContext(<DashboardPage />);

        const projectNameElem = await waitForElement(() =>
            getByText(/test project/i),
        );

        expect(projectNameElem).toHaveStyle('text-decoration: line-through');
    });

    it('shows a warning badge when a project is over budget', async () => {
        fetchMock.getOnce('/api/projects', [
            getMockProject({ is_over_budget: true }),
        ]);

        const { getByTestId } = renderWithContext(<DashboardPage />);

        const elem = await waitForElement(() =>
            getByTestId(/over-budget-badge/i),
        );

        expect(elem).toBeInTheDocument();
    });

    it('shows a list of tags related to the company', async () => {
        fetchMock.getOnce('/api/projects', [
            getMockProject({
                tags: [{ id: 1, name: 'Test Tag', color: 'primary' }],
            }),
        ]);

        const { getByText } = renderWithContext(<DashboardPage isLoading={false}/>);

        const elem = await waitForElement(() => getByText(/test tag/i));

        expect(elem).toBeInTheDocument();
    });

    it('shows a loading spinner while the projects are loading', async () => {
        fetchMock.getOnce('/api/projects', [getMockProject()]);

        const { getByTestId } = renderWithContext(<DashboardPage isLoading={true} />);

        expect(getByTestId('spinner')).toBeInTheDocument();
    });
});
